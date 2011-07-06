//
//  iOS_python_testAppDelegate.m
//  iOS-python-test
//
//  Created by Andrew Cobb on 12/5/10.
//  Copyright 2010 Andrew Cobb. All rights reserved.
//

#include "stdio.h"
#import "iOS_python_testAppDelegate.h"
#import "python2.6/Python.h"

@implementation iOS_python_testAppDelegate

@synthesize window;


#pragma mark -
#pragma mark Application lifecycle

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {    
    [self.window makeKeyAndVisible];
    
    NSLog(@"Trying to bootstrap python");
    //NSString *sprog = [[NSBundle mainBundle] pathForResource:@"YourApp/main" ofType:@"py"];
    const char * prog = [
                         [[NSBundle mainBundle] pathForResource:@"YourApp/main" ofType:@"py"] cStringUsingEncoding:
                         NSUTF8StringEncoding];
                        
    /**
    const char * prog = [[NSString stringWithContentsOfFile:[[NSBundle mainBundle] pathForResource:@"YourApp/main"
                                                                                            ofType:@"py"]
                                                   encoding:NSUTF8StringEncoding
                                                      error:nil] UTF8String];
/**/ 
    NSLog(@"Running main.py: %s", prog);
    FILE* fd = fopen(prog, "r");
    int ret = PyRun_SimpleFileEx(fd, prog, 1);
    if (ret != 0)
        NSLog(@"Application quit abnormally!");
    
    return YES;
}

- (void)dealloc {
    [window release];
    [super dealloc];
}


@end
