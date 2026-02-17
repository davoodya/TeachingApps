# Branch Descriptions

This document outlines the architectural differences between the branches in this repository.

## `main` Branch
In this branch, the application is implemented using a **Functional Programming** approach. The logic is structured around standalone functions that handle specific tasks such as sending data, receiving streams, and managing sockets. This approach provides a straightforward, procedural execution flow.

## `v2.0` Branch
In this branch, the application has been refactored and implemented using **Object-Oriented Programming (OOP)** principles. Key functionalities, such as hotkey management and connection handling, are encapsulated within classes (e.g., `HotkeyManager`). This structure enhances code modularity, scalability, and maintainability, allowing for better state management and easier extension of features.
