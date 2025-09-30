#!/usr/bin/env python3
import shutil
import subprocess
import os
import plistlib
import tempfile
import sys

def remove_all_signatures(app_path):
    """Elimina todas las firmas de código de la aplicación"""
    print("🚫 Eliminando todas las firmas de código...")
    
    # Eliminar firmas de la aplicación principal
    try:
        subprocess.run(["codesign", "--remove-signature", app_path], 
                      check=False, capture_output=True)
        print("   ✅ Firma principal eliminada")
    except Exception as e:
        print(f"   ⚠️  Error eliminando firma principal: {e}")
    
    # Eliminar directorios de firma
    for root, dirs, files in os.walk(app_path):
        if "_CodeSignature" in dirs:
            signature_dir = os.path.join(root, "_CodeSignature")
            try:
                shutil.rmtree(signature_dir)
                print(f"   ✅ Eliminado: {signature_dir}")
            except Exception as e:
                print(f"   ⚠️  Error eliminando {signature_dir}: {e}")
        
        if "CodeResources" in files:
            code_resources = os.path.join(root, "CodeResources")
            try:
                os.remove(code_resources)
                print(f"   ✅ Eliminado: {code_resources}")
            except Exception as e:
                print(f"   ⚠️  Error eliminando {code_resources}: {e}")
    
    # Eliminar firmas de frameworks
    frameworks_path = os.path.join(app_path, "Frameworks")
    if os.path.exists(frameworks_path):
        for framework in os.listdir(frameworks_path):
            if framework.endswith(".framework"):
                framework_path = os.path.join(frameworks_path, framework)
                try:
                    subprocess.run(["codesign", "--remove-signature", framework_path], 
                                  check=False, capture_output=True)
                    print(f"   ✅ Firma eliminada de: {framework}")
                except Exception as e:
                    print(f"   ⚠️  Error eliminando firma de {framework}: {e}")
    
    print("✅ Todas las firmas eliminadas")

def create_unsigned_app():
    """Crea una versión sin firmas de la aplicación"""
    original_app_path = "/Applications/HubSpot.app/Wrapper/HubSpot.app"
    
    print("============================================================")
    print("🚀 HUBSPOT CLONE - VERSIÓN SIN FIRMAS")
    print("============================================================")
    print("🚀 Creando versión sin firmas para ejecución local...")

    # Crear directorio temporal
    temp_dir = tempfile.mkdtemp(prefix="hubspot_unsigned_")
    modified_app_path = os.path.join(temp_dir, "HubSpot.app")

    print(f"📁 Directorio temporal: {temp_dir}")

    try:
        # Copiar la aplicación original
        print("📋 Copiando aplicación...")
        shutil.copytree(original_app_path, modified_app_path)
        print("✅ Aplicación copiada")

        # Aplicar modificaciones
        print("🔧 Aplicando modificaciones...")
        info_plist_path = os.path.join(modified_app_path, "Info.plist")
        
        if not os.path.exists(info_plist_path):
            print(f"❌ Error: Info.plist no encontrado en {info_plist_path}")
            return None

        with open(info_plist_path, 'rb') as fp:
            plist_data = plistlib.load(fp)
        
        # Modificar metadatos
        plist_data['CFBundleDisplayName'] = "HubSpot Local"
        plist_data['CFBundleIdentifier'] = "com.hubspot.CRMAppRelease.local"
        plist_data['CFBundleVersion'] = "1.0.0.local"
        plist_data['CFBundleShortVersionString'] = "1.0.0"
        
        with open(info_plist_path, 'wb') as fp:
            plistlib.dump(plist_data, fp)
        
        print("✅ Modificaciones aplicadas:")
        print(f"   - Nombre: {plist_data['CFBundleDisplayName']}")
        print(f"   - Bundle ID: {plist_data['CFBundleIdentifier']}")
        print(f"   - Versión: {plist_data['CFBundleShortVersionString']}")

        # Eliminar todas las firmas
        remove_all_signatures(modified_app_path)

        # Intentar re-firmar con firma ad-hoc
        print("✍️ Re-firmando con firma ad-hoc...")
        try:
            subprocess.run(["codesign", "--force", "--deep", "--sign", "-", modified_app_path], 
                          check=True, capture_output=True)
            print("✅ Re-firmado con éxito")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Error re-firmando: {e}")
            print("   Continuando sin firma...")

        return modified_app_path

    except Exception as e:
        print(f"❌ Error durante el proceso: {e}")
        return None

def launch_unsigned_app():
    """Ejecuta la aplicación sin firmas"""
    modified_app_path = create_unsigned_app()
    
    if not modified_app_path:
        print("❌ No se pudo crear la aplicación sin firmas")
        return

    print(f"\n🎯 Intentando ejecutar aplicación sin firmas...")
    print(f"📱 Ruta: {modified_app_path}")
    
    try:
        # Intentar ejecutar con open
        result = subprocess.run(["open", modified_app_path], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✨ ¡HubSpot sin firmas iniciado!")
            print("✅ La aplicación debería estar ejecutándose")
        else:
            print(f"❌ Error con 'open': {result.stderr.strip()}")
            
            # Intentar ejecutar el binario directamente
            print("\n🔄 Intentando ejecutar binario directamente...")
            executable_path = os.path.join(modified_app_path, "HubSpot")
            
            if os.path.exists(executable_path):
                print(f"💡 Ejecutable encontrado: {executable_path}")
                print("💡 Intentando ejecutar directamente...")
                
                try:
                    subprocess.run([executable_path], check=True)
                    print("✅ ¡Binario ejecutado directamente!")
                except subprocess.CalledProcessError as e:
                    print(f"❌ Error ejecutando binario: {e}")
                    print("💡 La aplicación puede requerir permisos especiales")
            else:
                print(f"❌ Ejecutable no encontrado en: {executable_path}")
                
                # Buscar otros ejecutables
                print("\n🔍 Buscando otros ejecutables...")
                for root, dirs, files in os.walk(modified_app_path):
                    for file in files:
                        if file in ["HubSpot", "HubSpotApp", "HubSpotAppRelease"]:
                            exec_path = os.path.join(root, file)
                            print(f"   📱 Encontrado: {exec_path}")
                            try:
                                subprocess.run([exec_path], check=True)
                                print(f"✅ ¡Ejecutado: {file}!")
                                return
                            except subprocess.CalledProcessError as e:
                                print(f"   ⚠️  Error ejecutando {file}: {e}")

    except Exception as e:
        print(f"❌ Error inesperado: {e}")

    print(f"\n📁 Directorio temporal: {modified_app_path}")
    print("💡 Puedes inspeccionar los archivos modificados en esa ubicación")

if __name__ == "__main__":
    launch_unsigned_app()
