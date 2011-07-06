//
//  main.m
//  iOS-python-test
//
//  Created by Andrew Cobb on 12/5/10.
//  Copyright 2010 Andrew Cobb. All rights reserved.
//

#import <UIKit/UIKit.h>
#include <python2.7/Python.h>
#include "SDL_main.h"


int main(int argc, char *argv[]) {
    NSLog(@"argc: %d", argc);
    NSLog(@"starting up");
    NSAutoreleasePool * pool = [[NSAutoreleasePool alloc] init];
    putenv("PYTHONOPTIMIZE=2");
    putenv("KIVY_WINDOW=sdl");
    putenv("KIVY_IMAGE=osxcoreimage");
    NSLog(@"initializing python");
    Py_Initialize();
    NSString * resourcePath = [[NSBundle mainBundle] resourcePath];
    NSLog(@"Setting python home");
    Py_SetPythonHome((char *)[resourcePath UTF8String]);
    NSLog(@"PythonHome is: %s", (char *)[resourcePath UTF8String]);
    PySys_SetArgv(argc, argv);

    NSLog(@"Trying to bootstrap python");
    const char * prog = [
                         [[NSBundle mainBundle] pathForResource:@"YourApp/main" ofType:@"py"] cStringUsingEncoding:
//                         [[NSBundle mainBundle] pathForResource:@"shader/plasma" ofType:@"py"] cStringUsingEncoding:
                         NSUTF8StringEncoding];

    NSLog(@"Running main.py: %s", prog);
    FILE* fd = fopen(prog, "r");
    int ret = PyRun_SimpleFileEx(fd, prog, 1);
    if (ret != 0)
        NSLog(@"Application quit abnormally!");
    
    Py_Finalize();
    NSLog(@"Leaving");
    [pool release];
    return ret;
}
