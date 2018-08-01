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
** SPDX License to detect: https://spdx.org/licenses/MirOS.html				
*/



/* SPDX-License-Identifier: MirOS */
/*
MirOS License

Copyright [YEAR] 
[NAME] [EMAIL] 

Provided that these
terms and disclaimer and all copyright notices are retained or
reproduced in an accompanying document, permission is granted to deal
in this work without restriction, including unlimited rights to use,
publicly perform, distribute, sell, modify, merge, give away, or
sublicence. 

This work is provided "AS IS" and WITHOUT WARRANTY of
any kind, to the utmost extent permitted by applicable law, neither
express nor implied; without malicious intent or gross negligence. In
no event may a licensor, author or contributor be held liable for
indirect, direct, other damage, loss, or other issues arising in any
way out of dealing in the work, even if advised of the possibility of
such damage or existence of a defect, except proven that it results
out of said person's immediate fault when using the work as intended.


I_N_S_T_R_U_C_T_I_O_N_S_:_ 
To apply the template(1) specify the
years of copyright (separated by comma, not as a range), the legal
names of the copyright holders, and the real names of the authors if
different. Avoid adding text.

R_A_T_I_O_N_A_L_E_:_ 
This licence is
apt for any kind of work (such as source code, fonts, documentation,
graphics, sound etc.) and the preferred terms for work added to
MirBSD. It has been drafted as universally usable equivalent of the
"historic permission notice"(2) adapted to Europen law because in some
(droit d'auteur) countries authors cannot disclaim all liabi‐
lities. Compliance to DFSG(3) 1.1 is ensured, and GPLv2 compatibility
is asserted unless advertising clauses are used. The MirOS Licence is
certified to conform to OKD(4) 1.0 and OSD(5) 1.9, and qualifies as a
Free Software(6) and also Free Documentation(7) licence and is
included in some relevant lists(8)(9)(10).

We believe you are not
liable for work inserted which is intellectual property of third
parties, if you were not aware of the fact, act appropriately as soon
as you become aware of that problem, seek an amicable solution for all
parties, and never knowingly distribute a work without being
authorised to do so by its licensors.

R_E_F_E_R_E_N_C_E_S_:_ 
(1)
also at http://mirbsd.de/MirOS-Licence 
(2)
http://www.opensource.org/licenses/historical.php 
(3)
http://www.debian.org/social_contract#guidelines 
(4)
http://www.opendefinition.org/1.0 
(5)
http://www.opensource.org/docs/osd 
(6)
http://www.gnu.org/philosophy/free-sw.html 
(7)
http://www.gnu.org/philosophy/free-doc.html 
(8)
http://www.ifross.de/ifross_html/lizenzcenter.html 
(9)
http://www.opendefinition.org/licenses 
(10)
http://opensource.org/licenses/miros.html
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

