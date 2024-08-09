from enum import Enum


class Languages(Enum):
    PYTHON = "Python"
    JAVA = "Java"
    RUBY = "Ruby"
    JAVASCRIPT = "Javascript"
    CSHARP = "C"
    CPP = "C"
    GOLANG = "Golang"
    PASCAL = "Pascal"
    KOTLIN = "Kotlin"
    SWIFT = "Swift"
    RUST = "Rust"
    PHP = "PHP"
    ASSEMBLY = "Assembly"
    C = "C"


class SexTypes(str, Enum):
    MALE = "Мужской"
    FEMALE = "Женский"
