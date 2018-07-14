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
** SPDX License to detect: https://spdx.org/licenses/MTLL.html				
*/



/* SPDX-License-Identifier: MTLL */
/*
Software License for MTL

Copyright (c) 2007 The Trustees of Indiana
University. 
     2008 Dresden University of Technology and the
Trustees of Indiana University. 
     2010 SimuNova UG
(haftungsbeschränkt), www.simunova.com. 
All rights reserved.

Authors: Peter Gottschling and Andrew Lumsdaine

This file is part of
the Matrix Template Library

Dresden University of Technology -- short
TUD -- and Indiana University -- short IU -- have the exclusive rights
to license this product under the following license.

Redistribution
and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:      
    
1. All redistributions of source code must retain the above copyright
notice, the list of authors in the original source code, this list of
conditions and the disclaimer listed in this license; 
     2. All
redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the disclaimer listed in this
license in the documentation and/or other materials provided with the
distribution; 
     3. Any documentation included with all
redistributions must include the following acknowledgement: 
    
"This product includes software developed at the University of Notre
Dame, the Pervasive Technology Labs at Indiana University, and Dresden
University of Technology. For technical information contact Andrew
Lumsdaine at the Pervasive Technology Labs at Indiana University. For
administrative and license questions contact the Advanced Research and
Technology Institute at 1100 Waterway Blvd. Indianapolis, Indiana
46202, phone 317-274-5905, fax 317-274-5902." 
     Alternatively,
this acknowledgement may appear in the software itself, and wherever
such third-party acknowledgments normally appear. 
     4. The name
"MTL" shall not be used to endorse or promote products derived from
this software without prior written permission from IU or TUD. For
written permission, please contact Indiana University Advanced
Research & Technology Institute. 
     5. Products derived from this
software may not be called "MTL", nor may "MTL" appear in their name,
without prior written permission of Indiana University Advanced
Research & Technology Institute.

TUD and IU provide no reassurances
that the source code provided does not infringe the patent or any
other intellectual property rights of any other entity. TUD and IU
disclaim any liability to any recipient for claims brought by any
other entity based on infringement of intellectual property rights or
otherwise. 

LICENSEE UNDERSTANDS THAT SOFTWARE IS PROVIDED "AS IS"
FOR WHICH NO WARRANTIES AS TO CAPABILITIES OR ACCURACY ARE MADE.
DRESDEN UNIVERSITY OF TECHNOLOGY AND INDIANA UNIVERSITY GIVE NO
WARRANTIES AND MAKE NO REPRESENTATION THAT SOFTWARE IS FREE OF
INFRINGEMENT OF THIRD PARTY PATENT, COPYRIGHT, OR OTHER PROPRIETARY
RIGHTS. DRESDEN UNIVERSITY OF TECHNOLOGY AND INDIANA UNIVERSITY MAKE
NO WARRANTIES THAT SOFTWARE IS FREE FROM "BUGS", "VIRUSES", "TROJAN
HORSES", "TRAP DOORS", "WORMS", OR OTHER HARMFUL CODE. LICENSEE
ASSUMES THE ENTIRE RISK AS TO THE PERFORMANCE OF SOFTWARE AND/OR
ASSOCIATED MATERIALS, AND TO THE PERFORMANCE AND VALIDITY OF
INFORMATION GENERATED USING SOFTWARE.
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

