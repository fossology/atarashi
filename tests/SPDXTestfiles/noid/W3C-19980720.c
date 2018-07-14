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
** SPDX License to detect: https://spdx.org/licenses/W3C-19980720.html				
*/



/*
W3C® SOFTWARE NOTICE AND LICENSE

Copyright (c) 1994-2002 World Wide
Web Consortium, (Massachusetts Institute of Technology, Institut
National de Recherche en Informatique et en Automatique, Keio
University). All Rights Reserved.
http://www.w3.org/Consortium/Legal/

This W3C work (including
software, documents, or other related items) is being provided by the
copyright holders under the following license. By obtaining, using
and/or copying this work, you (the licensee) agree that you have read,
understood, and will comply with the following terms and
conditions:

Permission to use, copy, modify, and distribute this
software and its documentation, with or without modification,  for
any purpose and without fee or royalty is hereby granted, provided
that you include the following on ALL copies of the software and
documentation or portions thereof, including modifications, that you
make:
	
     1.	The full text of this NOTICE in a location viewable to
users of the redistributed or derivative work.
	
     2.	Any
pre-existing intellectual property disclaimers, notices, or terms and
conditions. If none exist, a short notice of the following form
(hypertext is preferred, text is permitted) should be used within the
body of any redistributed or derivative code: "Copyright ©
[$date-of-software] World Wide Web Consortium, (Massachusetts
Institute of Technology, Institut National de Recherche en
Informatique et en Automatique, Keio University). All Rights Reserved.
http://www.w3.org/Consortium/Legal/"
	
      3. Notice of any changes
or modifications to the W3C files, including the date changes were
made. (We recommend you provide URIs to the location from which the
code is derived.)

THIS SOFTWARE AND DOCUMENTATION IS PROVIDED "AS
IS," AND COPYRIGHT HOLDERS MAKE NO REPRESENTATIONS OR WARRANTIES,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO, WARRANTIES OF
MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE
OF THE SOFTWARE OR DOCUMENTATION WILL NOT INFRINGE ANY THIRD PARTY
PATENTS, COPYRIGHTS, TRADEMARKS OR OTHER RIGHTS.

COPYRIGHT HOLDERS
WILL NOT BE LIABLE FOR ANY DIRECT, INDIRECT, SPECIAL OR CONSEQUENTIAL
DAMAGES ARISING OUT OF ANY USE OF THE SOFTWARE OR DOCUMENTATION.

The
name and trademarks of copyright holders may NOT be used in
advertising or publicity pertaining to the software without specific,
written prior permission. Title to copyright in this software and any
associated documentation will at all times remain with copyright
holders.

____________________________________

This formulation of
W3C's notice and license became active on August 14 1998 so as to
improve compatibility with GPL. This version ensures that W3C software
licensing terms are no more restrictive than GPL and consequently W3C
software may be distributed in GPL packages. See the older formulation
for the policy prior to this date. Please see our Copyright FAQ for
common questions about using materials from our site, including
specific terms and conditions for packages like libwww, Amaya, and
Jigsaw. Other questions about this notice can be directed to
site-policy@w3.org.
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

