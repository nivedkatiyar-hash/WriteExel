WriteExel README

What this is

WriteExel is an Android application that enables users to create and write Excel files directly on Android devices. Built with Android Studio, it provides a simple interface for generating Excel spreadsheets using the Apache POI library on mobile platforms.

Stack

Language: Java
Framework / runtime: Android SDK (minSdkVersion 21, targetSdkVersion 28), Gradle 3.5.0
Notable libraries: Apache POI 3.15 (poi, poi-ooxml, poi-ooxml-schemas), AndroidX (appcompat, constraintlayout)
How it's organized

Code
app/                      Main Android application module
  src/main/
    java/                 Java source code (com.anioncode.writeexel package)
    res/                  Android resources (layouts, strings, drawables)
    AndroidManifest.xml   App configuration and permissions
  libs/                   Local library dependencies
  build.gradle            App module build configuration

poi-3.15/                 Apache POI 3.15 library module
poi-ooxml-3.15/           POI OOXML support module
poi-ooxml-schemas-3.15/   POI OOXML schemas module

build.gradle              Root project build configuration
gradle.properties         Gradle build properties (AndroidX enablement)
settings.gradle           Multi-project configuration
How it fits together: This is a multi-module Android Gradle project that bundles Apache POI libraries locally to support Excel file generation on Android. The main app module (com.anioncode.writeexel) uses the POI libraries included in the three poi-* modules to provide Excel writing capabilities through a standard Android UI.

How to run it

Build the project:

bash
./gradlew build
Install and run on an Android device or emulator:

bash
./gradlew installDebug
Run tests:

bash
./gradlew test
./gradlew connectedAndroidTest
Requirements:

Android SDK 21+ installed
Android device or emulator with API level 21 or higher
Java JDK for building
