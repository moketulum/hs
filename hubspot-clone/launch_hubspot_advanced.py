#!/usr/bin/env python3
"""
HubSpot Clone - Advanced Launcher
Intenta ejecutar HubSpot con modificaciones locales y manejo mejorado de firmas
"""

import shutil
import subprocess
import os
import plistlib
import tempfile
import sys
from pathlib import Path

def check_developer_tools():
    """Verifica si las herramientas de desarrollador están disponibles"""
    try:
        result = subprocess.run(['xcode-select', '--print-path'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Xcode Command Line Tools: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Xcode Command Line Tools no encontrados")
        return False

def create_self_signed_certificate():
    """Crea un certificado auto-firmado para firmar la aplicación"""
    try:
        # Verificar si ya existe un certificado
        result = subprocess.run(['security', 'find-identity', '-v', '-p', 'codesigning'], 
                              capture_output=True, text=True)
        
        if "0 valid identities found" not in result.stdout:
            print("✅ Certificado de firma encontrado")
            return True
            
        print("🔐 Creando certificado auto-firmado...")
        
        # Crear certificado auto-firmado
        cert_script = '''
        #!/bin/bash
        # Crear certificado auto-firmado
        security create-keypair -a "HubSpot Clone Developer" -s -k login.keychain
        security add-trusted-cert -d -r trustRoot -k login.keychain hubspot-clone.crt
        '''
        
        with open('/tmp/create_cert.sh', 'w') as f:
            f.write(cert_script)
        
        os.chmod('/tmp/create_cert.sh', 0o755)
        subprocess.run(['/tmp/create_cert.sh'], check=True)
        
        print("✅ Certificado creado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error creando certificado: {e}")
        return False

def sign_application(app_path):
    """Firma la aplicación con certificado"""
    try:
        print("🔐 Firmando aplicación...")
        
        # Buscar certificado disponible
        result = subprocess.run(['security', 'find-identity', '-v', '-p', 'codesigning'], 
                              capture_output=True, text=True)
        
        if "0 valid identities found" in result.stdout:
            print("⚠️  No se encontraron certificados de firma")
            return False
            
        # Obtener el primer certificado disponible
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if ')' in line and '"' in line:
                cert_id = line.split(')')[0].strip()
                break
        else:
            print("❌ No se pudo encontrar certificado válido")
            return False
            
        # Firmar la aplicación
        sign_cmd = [
            'codesign', '--force', '--sign', cert_id,
            '--deep', '--timestamp', '--options', 'runtime',
            app_path
        ]
        
        result = subprocess.run(sign_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Aplicación firmada exitosamente")
            return True
        else:
            print(f"❌ Error firmando aplicación: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error en proceso de firma: {e}")
        return False

def launch_modified_hubspot():
    """Lanza HubSpot con modificaciones locales"""
    original_app_path = "/Applications/HubSpot.app"
    
    if not os.path.exists(original_app_path):
        print("❌ HubSpot no encontrado en /Applications/")
        return False
    
    print("🚀 Iniciando HubSpot con modificaciones locales...")
    
    # Verificar herramientas de desarrollador
    if not check_developer_tools():
        print("💡 Instala Xcode Command Line Tools: xcode-select --install")
        return False
    
    # Crear directorio temporal
    temp_dir = tempfile.mkdtemp(prefix="hubspot_modified_")
    modified_app_path = os.path.join(temp_dir, "HubSpot.app")
    
    print(f"📁 Directorio temporal: {temp_dir}")
    
    try:
        # Copiar la aplicación original
        print("📋 Copiando aplicación...")
        shutil.copytree(original_app_path, modified_app_path)
        
        # Aplicar modificaciones
        print("🔧 Aplicando modificaciones...")
        info_plist_path = os.path.join(modified_app_path, "Contents", "Info.plist")
        
        # Leer y modificar Info.plist
        with open(info_plist_path, 'rb') as fp:
            plist_data = plistlib.load(fp)
        
        # Modificaciones
        plist_data['CFBundleDisplayName'] = "HubSpot Clone"
        plist_data['CFBundleIdentifier'] = "com.hubspot.CRMAppRelease.clone"
        plist_data['CFBundleName'] = "HubSpot Clone"
        
        # Guardar Info.plist modificado
        with open(info_plist_path, 'wb') as fp:
            plistlib.dump(plist_data, fp)
        
        print("✅ Modificaciones aplicadas:")
        print(f"   - Nombre: {plist_data['CFBundleDisplayName']}")
        print(f"   - Bundle ID: {plist_data['CFBundleIdentifier']}")
        
        # Remover firmas existentes
        print("🚫 Removiendo firmas existentes...")
        subprocess.run(["codesign", "--remove-signature", modified_app_path], 
                      capture_output=True)
        
        # Eliminar directorios de firma
        for root, dirs, files in os.walk(modified_app_path):
            if "_CodeSignature" in dirs:
                shutil.rmtree(os.path.join(root, "_CodeSignature"))
            if "CodeResources" in files:
                os.remove(os.path.join(root, "CodeResources"))
        
        # Intentar crear certificado si es necesario
        create_self_signed_certificate()
        
        # Firmar la aplicación
        if sign_application(modified_app_path):
            # Intentar ejecutar
            print(f"🎯 Ejecutando: {modified_app_path}")
            result = subprocess.run(["open", modified_app_path], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✨ ¡HubSpot Clone iniciado exitosamente!")
                print("💡 La aplicación se ejecutará con las modificaciones aplicadas")
                return True
            else:
                print(f"❌ Error al ejecutar: {result.stderr}")
                
                # Intentar ejecutar directamente el binario
                binary_path = os.path.join(modified_app_path, "Contents", "MacOS", "HubSpot")
                if os.path.exists(binary_path):
                    print("🔄 Intentando ejecutar binario directamente...")
                    try:
                        subprocess.Popen([binary_path])
                        print("✨ ¡HubSpot Clone iniciado directamente!")
                        return True
                    except Exception as e:
                        print(f"❌ Error ejecutando binario: {e}")
        else:
            print("❌ No se pudo firmar la aplicación")
            
        # Mostrar información de depuración
        print("\n🔍 Información de depuración:")
        print(f"   - App path: {modified_app_path}")
        print(f"   - Binary exists: {os.path.exists(os.path.join(modified_app_path, 'Contents', 'MacOS', 'HubSpot'))}")
        print(f"   - Info.plist exists: {os.path.exists(info_plist_path)}")
        
        return False
        
    except Exception as e:
        print(f"❌ Error durante el proceso: {e}")
        return False
    
    finally:
        # Mantener el directorio temporal para inspección
        print(f"\n📁 Directorio temporal mantenido para inspección: {temp_dir}")
        print("💡 Puedes inspeccionar los archivos modificados en esa ubicación")

def main():
    """Función principal"""
    print("=" * 60)
    print("🚀 HUBSPOT CLONE - LAUNCHER AVANZADO")
    print("=" * 60)
    
    success = launch_modified_hubspot()
    
    if success:
        print("\n✅ ¡Proceso completado exitosamente!")
    else:
        print("\n❌ El proceso falló. Revisa los mensajes de error arriba.")
        print("\n💡 Alternativas:")
        print("   1. Usar HubSpot original: open /Applications/HubSpot.app")
        print("   2. Implementar tu propia versión usando la documentación")
        print("   3. Instalar certificados de desarrollador de Apple")

if __name__ == "__main__":
    main()
