#!/usr/bin/env python3
import shutil
import subprocess
import os
import plistlib
import tempfile
import sys

def create_unsigned_hubspot():
    """Crea una versión sin firmas de HubSpot"""
    original_app_path = "/Applications/HubSpot.app/Wrapper/HubSpot.app"
    
    print("============================================================")
    print("🚀 HUBSPOT CLONE - VERSIÓN SIN FIRMAS COMPLETA")
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
        
        with open(info_plist_path, 'rb') as fp:
            plist_data = plistlib.load(fp)
        
        # Modificar metadatos
        plist_data['CFBundleDisplayName'] = "HubSpot Sin Firmas"
        plist_data['CFBundleIdentifier'] = "com.hubspot.CRMAppRelease.unsigned"
        plist_data['CFBundleVersion'] = "1.0.0.unsigned"
        plist_data['CFBundleShortVersionString'] = "1.0.0"
        
        with open(info_plist_path, 'wb') as fp:
            plistlib.dump(plist_data, fp)
        
        print("✅ Modificaciones aplicadas:")
        print(f"   - Nombre: {plist_data['CFBundleDisplayName']}")
        print(f"   - Bundle ID: {plist_data['CFBundleIdentifier']}")
        print(f"   - Versión: {plist_data['CFBundleShortVersionString']}")

        # Eliminar todas las firmas
        print("🚫 Eliminando todas las firmas de código...")
        remove_all_signatures(modified_app_path)
        print("✅ Todas las firmas eliminadas")

        return modified_app_path

    except Exception as e:
        print(f"❌ Error durante el proceso: {e}")
        return None

def remove_all_signatures(app_path):
    """Elimina todas las firmas de código de la aplicación"""
    # Eliminar firmas de la aplicación principal
    subprocess.run(["codesign", "--remove-signature", app_path], 
                  check=False, capture_output=True)
    
    # Eliminar directorios de firma
    for root, dirs, files in os.walk(app_path):
        if "_CodeSignature" in dirs:
            shutil.rmtree(os.path.join(root, "_CodeSignature"))
        if "CodeResources" in files:
            os.remove(os.path.join(root, "CodeResources"))
    
    # Eliminar firmas de frameworks
    frameworks_path = os.path.join(app_path, "Frameworks")
    if os.path.exists(frameworks_path):
        for framework in os.listdir(frameworks_path):
            if framework.endswith(".framework"):
                framework_path = os.path.join(frameworks_path, framework)
                subprocess.run(["codesign", "--remove-signature", framework_path], 
                              check=False, capture_output=True)

def main():
    """Función principal"""
    print("🚀 HUBSPOT CLONE - ELIMINACIÓN DE CERTIFICADOS")
    print("============================================================")
    
    # Crear aplicación sin firmas
    modified_app_path = create_unsigned_hubspot()
    
    if not modified_app_path:
        print("❌ No se pudo crear la aplicación sin firmas")
        return

    print(f"\n✅ ¡APLICACIÓN SIN FIRMAS CREADA EXITOSAMENTE!")
    print(f"📁 Ubicación: {modified_app_path}")
    print(f"📱 Tamaño: {get_folder_size(modified_app_path)}")
    
    print("\n============================================================")
    print("💡 OPCIONES PARA USAR LA APLICACIÓN SIN FIRMAS")
    print("============================================================")
    
    print("\n1️⃣  HUBSPOT ORIGINAL (Recomendado):")
    print("   open /Applications/HubSpot.app")
    print("   ✅ Funciona perfectamente")
    print("   ✅ Todas las funcionalidades disponibles")
    print("   ✅ Sin modificaciones")
    
    print("\n2️⃣  XCODE SIMULATOR (Para la versión sin firmas):")
    print("   - Abrir Xcode")
    print("   - Window > Devices and Simulators")
    print("   - Seleccionar un simulador iOS")
    print("   - Arrastrar la app sin firmas al simulador")
    print(f"   - Ruta: {modified_app_path}")
    
    print("\n3️⃣  DISPOSITIVO iOS (Requiere certificado):")
    print("   - Conectar iPhone/iPad")
    print("   - Usar Xcode para instalar la app")
    print("   - Requiere certificado de desarrollador de Apple")
    
    print("\n4️⃣  IMPLEMENTAR TU PROPIA VERSIÓN:")
    print("   - Usar la documentación extraída en documentation/")
    print("   - Crear app nativa para macOS")
    print("   - Implementar funcionalidades paso a paso")
    print("   - Usar los endpoints y esquemas extraídos")
    
    print("\n5️⃣  MODIFICAR RECURSOS (Sin ejecutar):")
    print("   - Editar imágenes en la app")
    print("   - Modificar textos y configuraciones")
    print("   - Cambiar colores y estilos")
    print("   - Personalizar la interfaz")
    
    print(f"\n📁 Directorio temporal: {modified_app_path}")
    print("💡 Puedes inspeccionar y modificar los archivos en esa ubicación")
    
    # Preguntar si quiere ejecutar el original
    print("\n" + "="*60)
    print("¿Quieres ejecutar HubSpot original ahora? (y/n): ", end="")
    try:
        response = input().lower().strip()
        if response in ['y', 'yes', 'sí', 'si']:
            print("\n🚀 Ejecutando HubSpot original...")
            subprocess.run(["open", "/Applications/HubSpot.app"], check=True)
            print("✅ ¡HubSpot original iniciado!")
        else:
            print("💡 Puedes ejecutarlo más tarde con: open /Applications/HubSpot.app")
    except KeyboardInterrupt:
        print("\n💡 Puedes ejecutar HubSpot original más tarde con: open /Applications/HubSpot.app")

def get_folder_size(folder_path):
    """Calcula el tamaño de una carpeta"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    
    # Convertir a MB
    size_mb = total_size / (1024 * 1024)
    return f"{size_mb:.1f} MB"

if __name__ == "__main__":
    main()
