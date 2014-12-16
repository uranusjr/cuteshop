========
Usage
========

Cuteshop is mainly designed to be used as an executable. A script called
``cuteshop`` should already be installed to your ``PATH``. To use it, you need
to create a ``Shopfile`` in your project directory::

    packages:
        - hoedown

This is essentially YAML data, with all packages you wish to install listed
under that ``packages`` key.

Now run ``cuteshop`` inside the project directory (the same that contains
``Shopfile``). All dependencies will be fetched into subdirectory ``3rdparty``.
Cureshop automatically generates a ``subdir`` project for you; you can then add
it as a subproject to build with your main sources. All libraries will be built
statically and put into ``3rdparty/lib``, while headers go into
``3rdparty/include``.
