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
** SPDX License to detect: https://spdx.org/licenses/SAX-PD.html				
*/



/* SPDX-License-Identifier: SAX-PD */
/*
Copyright Status

SAX is free!

In fact, it's not possible to own a
license to SAX, since it's been placed in the public domain.

No
Warranty

Because SAX is released to the public domain, there is no
warranty for the design or for the software implementation, to the
extent permitted by applicable law. Except when otherwise stated in
writing the copyright holders and/or other parties provide SAX "as is"
without warranty of any kind, either expressed or implied, including,
but not limited to, the implied warranties of merchantability and
fitness for a particular purpose. The entire risk as to the quality
and performance of SAX is with you. Should SAX prove defective, you
assume the cost of all necessary servicing, repair or correction.

In
no event unless required by applicable law or agreed to in writing
will any copyright holder, or any other party who may modify and/or
redistribute SAX, be liable to you for damages, including any general,
special, incidental or consequential damages arising out of the use or
inability to use SAX (including but not limited to loss of data or
data being rendered inaccurate or losses sustained by you or third
parties or a failure of the SAX to operate with any other programs),
even if such holder or other party has been advised of the possibility
of such damages.

Copyright Disclaimers

This page includes statements
to that effect by David Megginson, who would have been able to claim
copyright for the original work.

SAX 1.0

Version 1.0 of the Simple
API for XML (SAX), created collectively by the membership of the
XML-DEV mailing list, is hereby released into the public domain.

No
one owns SAX: you may use it freely in both commercial and
non-commercial applications, bundle it with your software
distribution, include it on a CD-ROM, list the source code in a book,
mirror the documentation at your own web site, or use it in any other
way you see fit.

David Megginson, Megginson Technologies
Ltd.
1998-05-11

SAX 2.0

I hereby abandon any property rights to SAX
2.0 (the Simple API for XML), and release all of the SAX 2.0 source
code, compiled code, and documentation contained in this distribution
into the Public Domain. SAX comes with NO WARRANTY or guarantee of
fitness for any purpose.

David Megginson, Megginson Technologies
Ltd.
2000-05-05
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

