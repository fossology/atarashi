/*
** THIS IS A TEST FILE FOR THE SPDX LICENSE DETECTION TESTS											
**																										
** This file has been auto generated using the SPDX License List as represented by
** the JSON files:  https://github.com/spdx/license-list-data 
** 
** This file is for test purposes only. It WILL NOT compile or do anything useful otherwise.
**
** Test File Version: 1.0 No SPDX Identifiers - License List version 2.6
**
** DISCLAIMER
**
** Any copyrights appearing in this test file do so because they were part of the license text as stored by SPDX and are included 
** only for test purposes as they are part of the license text.	They have no meaning, implied or specific, otherwise.	
*/




/*
** LICENSE HEADER AND COPYRIGHT TO DETECT	
** This section either uses either the standard license header, or if one does not exist, the license 
** text as shown on the SPDX License List. In addition, if the file was generated using the write 
** license identifiers option, they will appear before the license text.
** 										
**
** SPDX License to detect: https://spdx.org/licenses/Eurosym.html				
*/



/* SPDX-License-Identifier: Eurosym */
/*
Copyright (c) 1999-2002 Henrik Theiling 
Licence Version 2

This
software is provided 'as-is', without warranty of any kind, express or
implied. In no event will the authors or copyright holders be held
liable for any damages arising from the use of this
software.

Permission is granted to anyone to use this software for
any purpose, including commercial applications, and to alter it and
redistribute it freely, subject to the following restrictions:

    
1. The origin of this software must not be misrepresented; you must
not claim that you wrote the original software. If you use this
software in a product, an acknowledgment in the product documentation
would be appreciated.

     2. Altered source versions must be plainly
marked as such, and must not be misrepresented as being the original
software.

     3. You must not use any of the names of the authors or
copyright holders of the original software for advertising or
publicity pertaining to distribution without specific, written prior
permission.

     4. If you change this software and redistribute
parts or all of it in any form, you must make the source code of the
altered version of this software available.

     5. This notice may
not be removed or altered from any source distribution.

This licence
is governed by the Laws of Germany. Disputes shall be settled by
Saarbruecken City Court.
*/

/*
** Fake code so we have something.
*/
#include <nothing.h>


int
noop_fun(int arg1)
{
	short retval;
	
	recalculatearg(&arg1);
	
	switch (arg1)
	{
		case 0:
			if (arg1) {
					retval = 1;
			} else {
			retval = 2;
			}
		case 1:
			retval = 2;
		case 2:
			retval = morpharg(arg1);
		case 3:
			if (arg1) {
				retval = 6;
			} else {
				retval = 7;
			}
		case 4:
			retval = upscalearg(arg1);
		default:
			retval = 0;
	}
	
	return retval;
}

