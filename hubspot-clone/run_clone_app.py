#!/usr/bin/env python3
import shutil
import subprocess
import os
import plistlib
import tempfile
import sys

def create_and_show_unsigned_app():
    """Crea una versión sin firmas y muestra las opciones"""
    original_app_path = "/Applications/HubSpot.app/Wrapper/HubSpot.app"
    
    print("============================================================")
    print("🚀 HUBSPOT CLONE - APLICACIÓN SIN CERTIFICADOS")
    print("============================================================")
    print("🚀 Creando versión sin firmas...")

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
        plist_data['CFBundleDisplayName'] = "HubSpot Sin Certificados"
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

def show_options(modified_app_path):
    """Muestra las opciones disponibles"""
    print("\n" + "="*60)
    print("💡 OPCIONES PARA USAR LA APLICACIÓN SIN CERTIFICADOS")
    print("="*60)
    
    print("\n1️⃣  HUBSPOT ORIGINAL (Recomendado - Funciona perfectamente):")
    print("   open /Applications/HubSpot.app")
    print("   ✅ Todas las funcionalidades disponibles")
    print("   ✅ Sin modificaciones")
    print("   ✅ Ejecutándose localmente")
    
    print(f"\n2️⃣  APLICACIÓN SIN CERTIFICADOS CREADA:")
    print(f"   📁 Ubicación: {modified_app_path}")
    print(f"   📱 Tamaño: {get_folder_size(modified_app_path)}")
    print("   ⚠️  Es una aplicación iOS, no se puede ejecutar directamente en macOS")
    
    print("\n3️⃣  XCODE SIMULATOR (Para la versión sin certificados):")
    print("   - Abrir Xcode")
    print("   - Window > Devices and Simulators")
    print("   - Seleccionar un simulador iOS")
    print("   - Arrastrar la app sin certificados al simulador")
    print(f"   - Ruta: {modified_app_path}")
    
    print("\n4️⃣  DISPOSITIVO iOS (Requiere certificado):")
    print("   - Conectar iPhone/iPad")
    print("   - Usar Xcode para instalar la app")
    print("   - Requiere certificado de desarrollador de Apple")
    
    print("\n5️⃣  IMPLEMENTAR TU PROPIA VERSIÓN:")
    print("   - Usar la documentación extraída en documentation/")
    print("   - Crear app nativa para macOS")
    print("   - Implementar funcionalidades paso a paso")
    print("   - Usar los endpoints y esquemas extraídos")
    
    print("\n6️⃣  MODIFICAR RECURSOS (Sin ejecutar):")
    print("   - Editar imágenes en la app")
    print("   - Modificar textos y configuraciones")
    print("   - Cambiar colores y estilos")
    print("   - Personalizar la interfaz")
    
    print(f"\n📁 Directorio temporal: {modified_app_path}")
    print("💡 Puedes inspeccionar y modificar los archivos en esa ubicación")

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

def main():
    """Función principal"""
    print("🚀 HUBSPOT CLONE - EJECUTANDO APLICACIÓN SIN CERTIFICADOS")
    print("============================================================")
    
    # Crear aplicación sin firmas
    modified_app_path = create_and_show_unsigned_app()
    
    if not modified_app_path:
        print("❌ No se pudo crear la aplicación sin firmas")
        return

    print(f"\n✅ ¡APLICACIÓN SIN CERTIFICADOS CREADA EXITOSAMENTE!")
    print(f"📁 Ubicación: {modified_app_path}")
    print(f"📱 Tamaño: {get_folder_size(modified_app_path)}")
    
    # Mostrar opciones
    show_options(modified_app_path)
    
    # Ejecutar HubSpot original automáticamente
    print("\n" + "="*60)
    print("🚀 EJECUTANDO HUBSPOT ORIGINAL AUTOMÁTICAMENTE...")
    print("="*60)
    
    try:
        print("🎯 Abriendo HubSpot original...")
        subprocess.run(["open", "/Applications/HubSpot.app"], check=True)
        print("✅ ¡HubSpot original iniciado exitosamente!")
        print("🎉 ¡La aplicación ya está funcionando en tu Mac!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando HubSpot original: {e}")
        print("💡 Intenta ejecutar manualmente: open /Applications/HubSpot.app")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
