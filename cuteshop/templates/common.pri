win32 {
    MKDIR = mkdir
}
else {
    MKDIR = mkdir -p
}

TEMPLATE = lib
CONFIG += staticlib

OBJECTS_DIR = build
MOC_DIR = build
RCC_DIR = build
UI_DIR = build
DESTDIR = ../../lib
