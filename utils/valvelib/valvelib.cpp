//========= Copyright Valve Corporation, All rights reserved. ============//
//
// Purpose: 
//
// $NoKeywords: $
//
//=============================================================================//
// valvelib.cpp : Defines the initialization routines for the DLL.
//

#include "stdafx.h"
#include <afxdllx.h>
#include "valvelib.h"
#include "valvelibaw.h"

#ifdef _PSEUDO_DEBUG
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

static AFX_EXTENSION_MODULE ValvelibDLL = { NULL, NULL };

extern "C" int APIENTRY
DllMain(HINSTANCE hInstance, DWORD dwReason, LPVOID lpReserved)
{
	if (dwReason == DLL_PROCESS_ATTACH)
	{
		TRACE0("VALVELIB.AWX Initializing!\n");
		
		// Extension DLL one-time initialization
		AfxInitExtensionModule(ValvelibDLL, hInstance);

		// Insert this DLL into the resource chain
		new CDynLinkLibrary(ValvelibDLL);

		// Register this custom AppWizard with MFCAPWZ.DLL
		SetCustomAppWizClass(&Valvelibaw);
	}
	else if (dwReason == DLL_PROCESS_DETACH)
	{
		TRACE0("VALVELIB.AWX Terminating!\n");

		// Terminate the library before destructors are called
		AfxTermExtensionModule(ValvelibDLL);
	}
	return 1;   // ok
}
