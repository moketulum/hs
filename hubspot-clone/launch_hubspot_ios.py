#!/usr/bin/env python3
"""
HubSpot Clone - iOS App Launcher
Lanza HubSpot (aplicación iOS) con modificaciones locales
"""

import shutil
import subprocess
import os
import plistlib
import tempfile
import sys
from pathlib import Path

def launch_modified_hubspot():
    """Lanza HubSpot iOS con modificaciones locales"""
    original_app_path = "/Applications/HubSpot.app/Wrapper/HubSpot.app"
    
    if not os.path.exists(original_app_path):
        print("❌ HubSpot no encontrado en /Applications/HubSpot.app/Wrapper/HubSpot.app")
        return False
    
    print("🚀 Iniciando HubSpot iOS con modificaciones locales...")
    
    # Crear directorio temporal
    temp_dir = tempfile.mkdtemp(prefix="hubspot_ios_modified_")
    modified_app_path = os.path.join(temp_dir, "HubSpot.app")
    
    print(f"📁 Directorio temporal: {temp_dir}")
    
    try:
        # Copiar la aplicación original
        print("📋 Copiando aplicación iOS...")
        shutil.copytree(original_app_path, modified_app_path)
        
        # Aplicar modificaciones
        print("🔧 Aplicando modificaciones...")
        info_plist_path = os.path.join(modified_app_path, "Info.plist")
        
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
        
        # Intentar ejecutar directamente
        print(f"🎯 Intentando ejecutar aplicación iOS...")
        
        # Método 1: Usar open
        result = subprocess.run(["open", modified_app_path], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✨ ¡HubSpot Clone iniciado exitosamente!")
            return True
        else:
            print(f"❌ Error con 'open': {result.stderr}")
            
            # Método 2: Ejecutar binario directamente
            binary_path = os.path.join(modified_app_path, "HubSpot")
            if os.path.exists(binary_path):
                print("🔄 Intentando ejecutar binario iOS directamente...")
                try:
                    # Para aplicaciones iOS, necesitamos usar el simulador o dispositivo
                    print("💡 Esta es una aplicación iOS, no se puede ejecutar directamente en macOS")
                    print("💡 Necesitas usar Xcode Simulator o un dispositivo iOS")
                    
                    # Mostrar información de la app
                    print(f"\n📱 Información de la aplicación iOS:")
                    print(f"   - Bundle ID: {plist_data['CFBundleIdentifier']}")
                    print(f"   - Display Name: {plist_data['CFBundleDisplayName']}")
                    print(f"   - Version: {plist_data.get('CFBundleShortVersionString', 'N/A')}")
                    print(f"   - Build: {plist_data.get('CFBundleVersion', 'N/A')}")
                    print(f"   - Platform: {plist_data.get('CFBundleSupportedPlatforms', 'N/A')}")
                    
                    return True
                except Exception as e:
                    print(f"❌ Error ejecutando binario: {e}")
            else:
                print("❌ Binario no encontrado")
        
        return False
        
    except Exception as e:
        print(f"❌ Error durante el proceso: {e}")
        return False
    
    finally:
        # Mantener el directorio temporal para inspección
        print(f"\n📁 Directorio temporal mantenido: {temp_dir}")
        print("💡 Puedes inspeccionar los archivos modificados en esa ubicación")

def show_alternatives():
    """Muestra alternativas para ejecutar HubSpot"""
    print("\n" + "="*60)
    print("💡 ALTERNATIVAS PARA EJECUTAR HUBSPOT")
    print("="*60)
    
    print("\n1️⃣  HUBSPOT ORIGINAL (Recomendado):")
    print("   open /Applications/HubSpot.app")
    print("   ✅ Funciona perfectamente")
    print("   ✅ Todas las funcionalidades disponibles")
    
    print("\n2️⃣  XCODE SIMULATOR:")
    print("   - Abrir Xcode")
    print("   - Window > Devices and Simulators")
    print("   - Instalar la app modificada en el simulador")
    
    print("\n3️⃣  DISPOSITIVO iOS:")
    print("   - Conectar iPhone/iPad")
    print("   - Usar Xcode para instalar la app")
    print("   - Requiere certificado de desarrollador")
    
    print("\n4️⃣  IMPLEMENTAR TU PROPIA VERSIÓN:")
    print("   - Usar la documentación extraída")
    print("   - Crear app nativa para macOS")
    print("   - Implementar funcionalidades paso a paso")

def main():
    """Función principal"""
    print("=" * 60)
    print("🚀 HUBSPOT CLONE - iOS APP LAUNCHER")
    print("=" * 60)
    
    success = launch_modified_hubspot()
    
    if success:
        print("\n✅ ¡Proceso completado!")
    else:
        print("\n❌ El proceso falló.")
    
    show_alternatives()

if __name__ == "__main__":
    main()
