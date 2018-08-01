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
** SPDX License to detect: https://spdx.org/licenses/Info-ZIP.html				
*/



/*
Info-ZIP License

Copyright (c) 1990-2009 Info-ZIP. All rights
reserved.

For the purposes of this copyright and license, "Info-ZIP"
is defined as the following set of individuals:

     Mark Adler, John
Bush, Karl Davis, Harald Denker, Jean-Michel Dubois, Jean-loup Gailly,
Hunter Goatley, Ed Gordon, Ian Gorman, Chris Herborth, Dirk Haase,
Greg Hartwig, Robert Heath, Jonathan Hudson, Paul Kienitz, David
Kirschbaum, Johnny Lee, Onno van der Linden, Igor Mandrichenko, Steve
P. Miller, Sergio Monesi, Keith Owens, George Petrov, Greg Roelofs,
Kai Uwe Rommel, Steve Salisbury, Dave Smith, Steven M. Schweda,
Christian Spieler, Cosmin Truta, Antoine Verheijen, Paul von Behren,
Rich Wales, Mike White.

This software is provided "as is," without
warranty of any kind, express or implied. In no event shall Info-ZIP
or its contributors be held liable for any direct, indirect,
incidental, special or consequential damages arising out of the use of
or inability to use this software.

Permission is granted to anyone to
use this software for any purpose, including commercial applications,
and to alter it and redistribute it freely, subject to the above
disclaimer and the following restrictions:

     *	Redistributions of
source code (in whole or in part) must retain the above copyright
notice, definition, disclaimer, and this list of conditions. 
    
*	Redistributions in binary form (compiled executables and libraries)
must reproduce the above copyright notice, definition, disclaimer, and
this list of conditions in documentation and/or other materials
provided with the distribution. Additional documentation is not needed
for executables where a command line license option provides these and
a note regarding this option is in the executable's startup banner.
The sole exception to this condition is redistribution of a standard
UnZipSFX binary (including SFXWiz) as part of a self-extracting
archive; that is permitted without inclusion of this license, as long
as the normal SFX banner has not been removed from the binary or
disabled. 
     *	Altered versions--including, but not limited to,
ports to new operating systems, existing ports with new graphical
interfaces, versions with modified or added functionality, and
dynamic, shared, or static library versions not from Info-ZIP--must be
plainly marked as such and must not be misrepresented as being the
original source or, if binaries, compiled from the original source.
Such altered versions also must not be misrepresented as being
Info-ZIP releases--including, but not limited to, labeling of the
altered versions with the names "Info-ZIP" (or any variation thereof,
including, but not limited to, different capitalizations), "Pocket
UnZip," "WiZ" or "MacZip" without the explicit permission of Info-ZIP.
Such altered versions are further prohibited from misrepresentative
use of the Zip-Bugs or Info-ZIP e-mail addresses or the Info-ZIP
URL(s), such as to imply Info-ZIP will provide support for the altered
versions. 
     *	Info-ZIP retains the right to use the names
"Info-ZIP," "Zip," "UnZip," "UnZipSFX," "WiZ," "Pocket UnZip," "Pocket
Zip," and "MacZip" for its own source and binary releases.
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

