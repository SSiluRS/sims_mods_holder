# Project: Sims Mode Holder

This project is a web application for managing and sharing mods for The Sims game series. It allows users to upload, categorize, and download mods, with support for tagging and filtering.

## General Instructions:
When generating code or answering questions, please adhere to the following guidelines:
1. **Code Style**: Follow PEP 8 guidelines for Python code. Use consistent indentation (4 spaces), meaningful variable names, and include docstrings for functions and classes.
2. **Database Interactions**: Use parameterized queries to prevent SQL injection. Ensure proper handling of database connections and cursors.
3. **Error Handling**: Implement robust error handling, especially for database operations and web requests. Use Flask's flash messaging system to provide user feedback.
4. **Frontend Development**: Use BEM (Block Element Modifier) methodology for CSS class naming. Ensure that HTML templates are clean and maintainable, leveraging Jinja2 features effectively.
5. **Security**: Do not expose sensitive information such as database credentials or secret keys in the codebase. Use environment variables for configuration.
6. **AJAX Support**: When implementing AJAX endpoints, check for the `X-Requested-With: XMLHttpRequest` header and return JSON responses as needed.
7. **Documentation**: Include comments and documentation where necessary to explain complex logic or decisions in the code.
8. **Security**: Dont seek into .env* files for sensitive information and dont edit this file.