# PyDotNetDev: Python Scripts for .NET Software Development with AI

This repository contains a collection of useful Python scripts designed to assist with various aspects of .NET software development, focusing on analysis, debugging, and integration, often leveraging AI-driven insights.

## 🔧 Tools by Category

### Avalonia .NET Tools
- `Avalonia.NET.Tools/AvaloniaProjectAnalyzer.py`: Analyzes Avalonia project structure, including `.csproj` and `.axaml` files, to identify missing files, resources, and structural issues.
- `Avalonia.NET.Tools/binding_analyzer.py`: Scans XAML for missing ViewModel bindings.
- `Avalonia.NET.Tools/XAML_Format_Error_Hunter.py`: Detects broken or malformed XAML.

### Codebase Structure Analysis
- `Codebase.Structure.Analysis/analyze_search_files.py`: Reviews search engine implementation files to identify strategy misalignment (job boards vs. company finding), missing Python script keywords, incomplete implementations, and files needing updates.
- `Codebase.Structure.Analysis/dependency_analyzer.py`: Analyzes C# file dependencies and relationships, including interfaces, classes, and DTOs, and suggests implementations for missing files.
- `Codebase.Structure.Analysis/jobfinder_repo_analyzer.py`: A comprehensive repository analyzer for the JobFinder project.

### Code Architecture Validation
- `Code.Architecture.Validation/structure_check.py`: Performs checks on the overall project's architectural structure.

### Data Model Analysis
- `Data.Model.Analysis/dto_structure_analyzer.py`: Examines the actual structure of DTOs, domain models, and enums, analyzing their properties, constructors, base classes, and implemented interfaces.

### Database Tools
- `Database.Tools/sqlite_diagnostic.py`: Provides diagnostic capabilities for SQLite databases.

### Dependency Injection Analysis
- `Dependency.Injection.Analysis/di_detective.py`: Analyzes your codebase, particularly `Program.cs`, to pinpoint specific Dependency Injection issues, such as incorrect service resolution (e.g., getting `SearchService` instead of `AdvancedSearchService`).

### Integration System Analysis
- `Integration.System.Analysis/Infrastructure_Analysis.py`: Analyzes the existing Infrastructure layer (search engines, scrapers, services, repositories) to identify necessary connections to the Core `SearchService` for a working search implementation.
- `Integration.System.Analysis/Integration_Gap_Analyzer.py`: Focuses on critical integration gaps related to `SearchService` usage with infrastructure search engines, Dependency Injection setup, missing method implementations, and interface mismatches.

### Project Health Diagnostics
- `Project.Health.Diagnostics/check.py`: A `JobAppAnalyzer` script that scans C# and XAML files, analyzes DTOs, repositories, and identifies missing services or corrupted files, providing a general health check.
- `Project.Health.Diagnostics/jobfinder_diagnostic_script.py`: Analyzes C# JobFinder system failures by comparing them with successful Python patterns, identifying critical fixes needed in areas like search engines, advanced search service, repositories, and database context.
- `Project.Health.Diagnostics/program_cs_analyzer.py`: Analyzes `Program.cs` for service registration issues.
- `Project.Health.Diagnostics/search_issue_analyzer.py`: Analyzes common search-related issues.
- `Project.Health.Diagnostics/search_debug_analyzer.py`: Provides advanced debugging for search functionalities.

### String Manipulation Utilities
- `String.Manipulation.Utilities/stringformat_finder.py`: Locates specific string formatting patterns.
- `String.Manipulation.Utilities/stringformat_fixer.py`: Automates fixes for identified string formatting issues.
