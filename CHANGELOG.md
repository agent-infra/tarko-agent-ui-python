# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite with 80%+ coverage requirement
- CI/CD pipeline with GitHub Actions
- Code quality tools (Black, isort, mypy)
- Contributing guidelines and development documentation
- Pull request template
- Type safety improvements

### Changed
- Enhanced error handling with more descriptive messages
- Improved documentation structure and examples
- Better project configuration with tool-specific settings

### Fixed
- Production readiness issues identified in review
- Missing test coverage for core functionality
- Inconsistent code formatting and style

## [0.3.0b11] - 2024-01-XX

### Added
- Initial Python SDK for serving Tarko Agent UI Builder static assets
- `get_static_path()` function to access bundled static files
- `get_agent_ui_html()` function with environment variable injection
- `inject_env_variables()` for customizing UI configuration
- FastAPI example with comprehensive UI configuration
- Automated asset downloading from npm registry
- Support for custom base URLs and UI configurations

### Features
- Framework-agnostic HTML generation
- Environment variable injection for runtime configuration
- Comprehensive error handling with actionable messages
- Support for complex nested UI configurations
- Offline operation after installation

### Documentation
- Complete README with usage examples
- Framework-specific integration examples (FastAPI, Flask, Django)
- API reference documentation
- Build script documentation

[Unreleased]: https://github.com/agent-infra/tarko-agent-ui-python/compare/v0.3.0b11...HEAD
[0.3.0b11]: https://github.com/agent-infra/tarko-agent-ui-python/releases/tag/v0.3.0b11
