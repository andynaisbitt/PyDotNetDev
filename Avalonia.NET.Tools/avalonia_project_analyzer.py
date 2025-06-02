#!/usr/bin/env python3
"""
Avalonia Project Diagnostic Script
Analyzes Avalonia project structure and identifies missing files/resources
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Set, Optional
import xml.etree.ElementTree as ET

class AvaloniaProjectAnalyzer:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.issues = []
        self.warnings = []
        self.info = []
        
    def analyze(self):
        """Run complete project analysis"""
        print("🔍 AVALONIA PROJECT DIAGNOSTIC ANALYSIS")
        print("=" * 60)
        
        self.check_project_structure()
        self.check_csproj_file()
        self.check_xaml_files()
        self.check_resources()
        self.check_app_files()
        self.check_build_artifacts()
        
        self.print_results()
        
    def check_project_structure(self):
        """Check basic project structure"""
        print("📁 Checking project structure...")
        
        required_files = [
            "*.csproj",
            "App.axaml",
            "App.axaml.cs"
        ]
        
        for pattern in required_files:
            matching_files = list(self.project_path.glob(pattern))
            if not matching_files:
                self.issues.append(f"Missing required file: {pattern}")
            else:
                self.info.append(f"Found: {matching_files[0].name}")
                
        # Check Views folder
        views_folder = self.project_path / "Views"
        if not views_folder.exists():
            self.warnings.append("Views folder doesn't exist")
        else:
            view_files = list(views_folder.glob("*.axaml"))
            self.info.append(f"Found {len(view_files)} view files")
            
        # Check Controls folder
        controls_folder = self.project_path / "Controls"
        if controls_folder.exists():
            control_files = list(controls_folder.glob("*.axaml"))
            self.info.append(f"Found {len(control_files)} control files")
            
    def check_csproj_file(self):
        """Analyze .csproj file for issues"""
        print("🔧 Checking project file...")
        
        csproj_files = list(self.project_path.glob("*.csproj"))
        if not csproj_files:
            self.issues.append("No .csproj file found")
            return
            
        csproj_path = csproj_files[0]
        try:
            tree = ET.parse(csproj_path)
            root = tree.getroot()
            
            # Check Avalonia packages
            avalonia_packages = []
            for item_group in root.findall(".//ItemGroup"):
                for package_ref in item_group.findall("PackageReference"):
                    include = package_ref.get("Include", "")
                    if "Avalonia" in include:
                        version = package_ref.get("Version", "Unknown")
                        avalonia_packages.append(f"{include} v{version}")
                        
            if avalonia_packages:
                self.info.append("Avalonia packages:")
                for pkg in avalonia_packages:
                    self.info.append(f"  - {pkg}")
            else:
                self.issues.append("No Avalonia packages found in project file")
                
            # Check for UseAvalonia property
            use_avalonia = root.find(".//UseAvalonia")
            if use_avalonia is None:
                self.warnings.append("UseAvalonia property not found in project file")
            elif use_avalonia.text != "true":
                self.issues.append("UseAvalonia property is not set to true")
                
        except ET.ParseError as e:
            self.issues.append(f"Failed to parse .csproj file: {e}")
            
    def check_xaml_files(self):
        """Check all XAML files for issues"""
        print("📄 Checking XAML files...")
        
        xaml_files = list(self.project_path.rglob("*.axaml"))
        self.info.append(f"Found {len(xaml_files)} XAML files")
        
        for xaml_file in xaml_files:
            self.check_single_xaml_file(xaml_file)
            
    def check_single_xaml_file(self, xaml_file: Path):
        """Check individual XAML file for common issues"""
        try:
            content = xaml_file.read_text(encoding='utf-8')
            
            # Check for empty files
            if not content.strip():
                self.issues.append(f"{xaml_file.name}: File is empty")
                return
                
            # Check for root element
            if not content.strip().startswith('<'):
                self.issues.append(f"{xaml_file.name}: No root element")
                return
                
            # Check for common typos
            typos = [
                ("ColumnDefinin", "ColumnDefinitions"),
                ("RowDefinin", "RowDefinitions"),
                ("MultiClass", "Classes"),
            ]
            
            for typo, correct in typos:
                if typo in content:
                    line_num = self.find_line_number(content, typo)
                    self.issues.append(f"{xaml_file.name}:{line_num}: Found '{typo}' (should be '{correct}')")
                    
            # Check for unsupported properties in Avalonia 11.0.7
            unsupported_props = [
                "ColumnGap", "RowGap", "Padding"
            ]
            
            for prop in unsupported_props:
                pattern = f'<StackPanel[^>]*{prop}='
                if re.search(pattern, content):
                    line_num = self.find_line_number(content, pattern)
                    if prop == "Padding":
                        self.issues.append(f"{xaml_file.name}:{line_num}: StackPanel doesn't support Padding (use Border instead)")
                    else:
                        self.issues.append(f"{xaml_file.name}:{line_num}: {prop} not supported in Avalonia 11.0.7 (use Margin instead)")
                        
            # Check x:Class declarations
            class_match = re.search(r'x:Class="([^"]+)"', content)
            if class_match:
                declared_class = class_match.group(1)
                expected_class = self.get_expected_class_name(xaml_file)
                if expected_class and declared_class != expected_class:
                    self.warnings.append(f"{xaml_file.name}: x:Class '{declared_class}' might not match file location (expected '{expected_class}')")
                    
        except Exception as e:
            self.issues.append(f"{xaml_file.name}: Failed to read file - {e}")
            
    def get_expected_class_name(self, xaml_file: Path) -> Optional[str]:
        """Get expected class name based on file location"""
        relative_path = xaml_file.relative_to(self.project_path)
        parts = list(relative_path.parts[:-1])  # Remove filename
        
        # Remove file extension
        class_name = xaml_file.stem
        
        # Build namespace
        if parts:
            namespace = "JobFinderApp.Desktop." + ".".join(parts)
        else:
            namespace = "JobFinderApp.Desktop"
            
        return f"{namespace}.{class_name}"
        
    def find_line_number(self, content: str, search_term: str) -> int:
        """Find line number of search term in content"""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if search_term in line:
                return i
        return 0
        
    def check_resources(self):
        """Check for resource files and references"""
        print("🖼️  Checking resources...")
        
        # Check Assets folder
        assets_folder = self.project_path / "Assets"
        if assets_folder.exists():
            asset_files = list(assets_folder.rglob("*"))
            asset_files = [f for f in asset_files if f.is_file()]
            self.info.append(f"Found {len(asset_files)} asset files")
        else:
            self.warnings.append("No Assets folder found")
            
        # Check Styles folder
        styles_folder = self.project_path / "Styles"
        if styles_folder.exists():
            style_files = list(styles_folder.glob("*.axaml"))
            self.info.append(f"Found {len(style_files)} style files")
            
            # Check for missing style references
            app_xaml = self.project_path / "App.axaml"
            if app_xaml.exists():
                app_content = app_xaml.read_text(encoding='utf-8')
                for style_file in style_files:
                    style_ref = f"Styles/{style_file.name}"
                    if style_ref not in app_content:
                        self.warnings.append(f"Style file {style_file.name} not referenced in App.axaml")
        else:
            self.info.append("No Styles folder found")
            
    def check_app_files(self):
        """Check App.axaml and App.axaml.cs specifically"""
        print("🚀 Checking application files...")
        
        app_xaml = self.project_path / "App.axaml"
        app_cs = self.project_path / "App.axaml.cs"
        
        if app_xaml.exists():
            try:
                content = app_xaml.read_text(encoding='utf-8')
                if not content.strip():
                    self.issues.append("App.axaml is empty")
                elif not "Application" in content:
                    self.issues.append("App.axaml doesn't contain Application root element")
                else:
                    self.info.append("App.axaml looks valid")
                    
                # Check for missing style includes
                if "StyleInclude" in content:
                    style_includes = re.findall(r'Source="([^"]+)"', content)
                    for style_path in style_includes:
                        full_path = self.project_path / style_path
                        if not full_path.exists():
                            self.issues.append(f"App.axaml references missing style: {style_path}")
                            
            except Exception as e:
                self.issues.append(f"Failed to read App.axaml: {e}")
        else:
            self.issues.append("App.axaml not found")
            
        if app_cs.exists():
            try:
                content = app_cs.read_text(encoding='utf-8')
                if "InitializeComponent" not in content:
                    self.warnings.append("App.axaml.cs doesn't call InitializeComponent()")
                self.info.append("App.axaml.cs exists")
            except Exception as e:
                self.issues.append(f"Failed to read App.axaml.cs: {e}")
        else:
            self.issues.append("App.axaml.cs not found")
            
    def check_build_artifacts(self):
        """Check build output and artifacts"""
        print("🔨 Checking build artifacts...")
        
        # Check obj folder
        obj_folder = self.project_path / "obj"
        if obj_folder.exists():
            # Look for generated files
            generated_files = list(obj_folder.rglob("*.g.cs"))
            if generated_files:
                self.info.append(f"Found {len(generated_files)} generated code files")
            else:
                self.warnings.append("No generated code files found (XAML might not be compiling)")
                
            # Check for Avalonia cache
            avalonia_cache = list(obj_folder.rglob("*avalonia*"))
            if avalonia_cache:
                self.info.append("Avalonia build cache exists")
        else:
            self.warnings.append("No obj folder found (project hasn't been built)")
            
        # Check bin folder
        bin_folder = self.project_path / "bin"
        if bin_folder.exists():
            exe_files = list(bin_folder.rglob("*.exe"))
            if exe_files:
                self.info.append(f"Found {len(exe_files)} executable files")
        else:
            self.warnings.append("No bin folder found")
            
    def print_results(self):
        """Print analysis results"""
        print("\n" + "=" * 60)
        print("📊 ANALYSIS RESULTS")
        print("=" * 60)
        
        if self.issues:
            print(f"\n❌ CRITICAL ISSUES ({len(self.issues)}):")
            for i, issue in enumerate(self.issues, 1):
                print(f"   {i}. {issue}")
                
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"   {i}. {warning}")
                
        if self.info:
            print(f"\n✅ INFO ({len(self.info)}):")
            for i, info in enumerate(self.info, 1):
                print(f"   {i}. {info}")
                
        print(f"\n🎯 SUMMARY:")
        print(f"   Issues: {len(self.issues)} | Warnings: {len(self.warnings)} | Info: {len(self.info)}")
        
        if self.issues:
            print(f"\n🔧 RECOMMENDED ACTIONS:")
            print("   1. Fix all critical issues first")
            print("   2. Address warnings that might affect functionality")
            print("   3. Clean and rebuild project")
            print("   4. Test application startup")

def main():
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = input("Enter path to Avalonia project directory: ")
        
    if not os.path.exists(project_path):
        print(f"❌ Error: Path '{project_path}' does not exist")
        return
        
    analyzer = AvaloniaProjectAnalyzer(project_path)
    analyzer.analyze()

if __name__ == "__main__":
    main()
