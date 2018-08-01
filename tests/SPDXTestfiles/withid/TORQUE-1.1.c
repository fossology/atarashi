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
** SPDX License to detect: https://spdx.org/licenses/TORQUE-1.1.html				
*/



/* SPDX-License-Identifier: TORQUE-1.1 */
/*
TORQUE v2.5+ Software License v1.1 
Copyright (c) 2010-2011 Adaptive
Computing Enterprises, Inc. All rights reserved.  

Use this license
to use or redistribute the TORQUE software v2.5+ and later versions.
For free support for TORQUE users, questions should be emailed to the
community of TORQUE users at torqueusers@supercluster.org. Users can
also subscribe to the user mailing list at
http://www.supercluster.org/mailman/listinfo/torqueusers. Customers
using TORQUE that also are licensed users of Moab branded software
from Adaptive Computing Inc. can get TORQUE support from Adaptive
Computing via: 
Email: torque-support@adaptivecomputing.com. 
Phone:
(801) 717-3700 
Web: www.adaptivecomputing.com
www.clusterresources.com 

This license covers use of the TORQUE v2.5
software (the "Software") at your site or location, and, for certain
users, redistribution of the Software to other sites and locations1.
Later versions of TORQUE are also covered by this license. Use and
redistribution of TORQUE v2.5 in source and binary forms, with or
without modification, are permitted provided that all of the following
conditions are met. 

1. Any Redistribution of source code must retain
the above copyright notice and the acknowledgment contained in
paragraph 5, this list of conditions and the disclaimer contained in
paragraph 5. 

2. Any Redistribution in binary form must reproduce the
above copyright notice and the acknowledgment contained in paragraph
4, this list of conditions and the disclaimer contained in paragraph 5
in the documentation and/or other materials provided with the
distribution. 

3. Redistributions in any form must be accompanied by
information on how to obtain complete source code for TORQUE and any
modifications and/or additions to TORQUE. The source code must either
be included in the distribution or be available for no more than the
cost of distribution plus a nominal fee, and all modifications and
additions to the Software must be freely redistributable by any party
(including Licensor) without restriction. 

4. All advertising
materials mentioning features or use of the Software must display the
following acknowledgment: 
"TORQUE is a modification of OpenPBS which
was developed by NASA Ames Research Center, Lawrence Livermore
National Laboratory, and Veridian TORQUE Open Source License v1.1. 1
Information Solutions, Inc. Visit www.clusterresources.com/products/
for more information about TORQUE and to download TORQUE. For
information about Moab branded products and so receive support from
Adaptive Computing for TORQUE, see www.adaptivecomputing.com.” 

5.
DISCLAIMER OF WARRANTY THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT
WARRANTY OF ANY KIND. ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT ARE EXPRESSLY
DISCLAIMED. IN NO EVENT SHALL ADAPTIVE COMPUTING ENTERPRISES, INC.
CORPORATION, ITS AFFILIATED COMPANIES, OR THE U.S. GOVERNMENT OR ANY
OF ITS AGENCIES BE LIABLE FOR ANY DIRECT OR INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


This license will be governed by the laws of Utah, without reference
to its choice of law rules. 

Note 1: TORQUE is developed from an
earlier version v2.3 of OpenPBS. TORQUE has been developed beyond
OpenPBS v2.3. The OpenPBS v2.3 license and OpenPBS software can be
obtained at:

http://www.pbsworks.com/ResLibSearchResult.aspx?keywords=openpbs&industry=All&pro
duct_service=All&category=Free%20Software%20Downloads&order_by=title.
Users of TORQUE should comply with the TORQUE license as well as the
OpenPBS license.
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

