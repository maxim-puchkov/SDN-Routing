//
//  main.cpp
//  SDNetworkLauncher
//
//  Created by admin on 2019-11-19.
//  Copyright © 2019 Maxim Puchkov. All rights reserved.
//
#define PY_SSIZE_T_CLEAN

#include <iostream>
#include <opencv2/core.hpp>
#include <Python/Python.h>
#include <Python/pythonrun.h>

const char *SCRIPT_NAME = "main.py";
const char *SCRIPT_PATH = "";

int main(int argc, char **argv) {
	Py_Initialize();
	Py_SetProgramName(argv[0]);  /* optional but recommended */
	std::cout << argv[0] << '\n';
	PyRun_SimpleString("from time import time,ctime\n"
					   "print 'Today is',ctime(time())\n");
	PyRun_SimpleString("from TestNet import *\n"
					   "print 'ok'\n");
	Py_Finalize();
	return 0;
}
