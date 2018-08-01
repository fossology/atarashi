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
** SPDX License to detect: https://spdx.org/licenses/SMPPL.html				
*/



/*
Secure Messaging Protocol (SMP) Libraries [ACL, CML,
SFL]

Distribution Rights 

All source code for the SMP is being
provided at no cost and with no financial limitations regarding its
use and distribution. Organizations can use the SMP without paying any
royalties or licensing fees. The SMP was originally developed by the
U.S. Government. BAE Systems is enhancing and supporting the SMP under
contract to the U.S. Government. The U.S. Government is furnishing the
SMP software at no cost to the vendor subject to the conditions of the
SMP Public License provided with the SMP software. 

29 May
2002

Secure Messaging Protocol (SMP) Public License

The United
States Government/Department of Defense/National Security
Agency/Office of Network Security (collectively "the U.S. Government")
hereby grants permission to any person obtaining a copy of the SMP
source and object files (the "SMP Software") and associated
documentation files (the "SMP Documentation"), or any portions
thereof, to do the following, subject to the following license
conditions:

You may, free of charge and without additional permission
from the U.S. Government, use, copy, modify, sublicense and otherwise
distribute the SMP Software or components of the SMP Software, with or
without modifications developed by you and/or by others.

You may,
free of charge and without additional permission from the U.S.
Government, distribute copies of the SMP Documentation, with or
without modifications developed by you and/or by others, at no charge
or at a charge that covers the cost of reproducing such copies,
provided that this SMP Public License is retained.

Furthermore, if
you distribute the SMP Software or parts of the SMP Software, with or
without modifications developed by you and/or others, then you must
either make available the source code to all portions of the SMP
Software (exclusive of any modifications made by you and/or by others)
upon request, or instead you may notify anyone requesting the SMP
Software source code that it is freely available from the U.S.
Government.

Transmission of this SMP Public License must accompany
whatever portions of the SMP Software you redistribute.

The SMP
Software is provided without warranty or guarantee of any nature,
express or implied, including without limitation the warranties of
merchantability and fitness for a particular purpose.

The U.S.
Government cannot be held liable for any damages either directly or
indirectly caused by the use of the SMP Software.

It is not permitted
to copy, sublicense, distribute or transfer any of the SMP Software
except as expressly indicated herein.  Any attempts to do otherwise
will be considered a violation of this License and your rights to the
SMP Software will be voided.

The SMP uses the Enhanced SNACC (eSNACC)
Abstract Syntax Notation One (ASN.1) C++ Library to ASN.1 encode and
decode security-related data objects.  The eSNACC ASN.1 C++ Library is
covered by the ENHANCED SNACC SOFTWARE PUBLIC LICENSE.  None of the
GNU public licenses apply to the eSNACC ASN.1 C++ Library.  The eSNACC
Compiler is not distributed as part of the SMP.

Copyright ©
1997-2002 National Security Agency
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

