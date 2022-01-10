//========= Copyright Valve Corporation, All rights reserved. ============//
//
// Purpose: 
//
//=============================================================================

#include "cbase.h"
#include "tf_weapon_bonesaw.h"
#include "tf_weapon_medigun.h"
#ifdef GAME_DLL
#include "tf_player.h"
#else
#include "c_tf_player.h"
#endif


#define UBERSAW_CHARGE_POSEPARAM		"syringe_charge_level"

//=============================================================================
//
// Weapon Bonesaw tables.
//

IMPLEMENT_NETWORKCLASS_ALIASED( TFBonesaw, DT_TFWeaponBonesaw )

BEGIN_NETWORK_TABLE( CTFBonesaw, DT_TFWeaponBonesaw )
END_NETWORK_TABLE()

BEGIN_PREDICTION_DATA( CTFBonesaw )
END_PREDICTION_DATA()

LINK_ENTITY_TO_CLASS( tf_weapon_bonesaw, CTFBonesaw );
PRECACHE_WEAPON_REGISTER( tf_weapon_bonesaw );

//-----------------------------------------------------------------------------
// Purpose: 
//-----------------------------------------------------------------------------
void CTFBonesaw::Activate( void )
{
	BaseClass::Activate();
}
//-----------------------------------------------------------------------------
void CTFBonesaw::SecondaryAttack( void )
{
	CTFPlayer *pPlayer = GetTFPlayerOwner();
	if ( !pPlayer )
		return;

#ifdef GAME_DLL
	int iSpecialTaunt = 0;
	CALL_ATTRIB_HOOK_INT( iSpecialTaunt, special_taunt );
	if ( iSpecialTaunt )
	{
		pPlayer->Taunt( TAUNT_BASE_WEAPON );
		return;
	}
#endif
	BaseClass::SecondaryAttack();
}
//-----------------------------------------------------------------------------
// Purpose: 
//-----------------------------------------------------------------------------
bool CTFBonesaw::DefaultDeploy( char *szViewModel, char *szWeaponModel, int iActivity, char *szAnimExt )
{
	if ( BaseClass::DefaultDeploy( szViewModel, szWeaponModel, iActivity, szAnimExt ) )
	{
#ifdef CLIENT_DLL
		UpdateChargePoseParam();
#endif
		return true;
	}

	return false;
}

//-----------------------------------------------------------------------------
void CTFBonesaw::DoMeleeDamage( CBaseEntity* ent, trace_t& trace )
{
	// We hit a target, take a head
	CTFPlayer *pPlayer = ToTFPlayer( GetOwnerEntity() );
	CTFPlayer *pVictim = ToTFPlayer( ent );
	
	int iTakeHeads = 0;
	CALL_ATTRIB_HOOK_INT( iTakeHeads, add_head_on_hit );
	if ( pPlayer && pVictim && iTakeHeads && (pVictim->GetTeamNumber() != pPlayer->GetTeamNumber() ) )
	{
		int iDecaps = pPlayer->m_Shared.GetDecapitations() + 1;
		pPlayer->m_Shared.SetDecapitations( iDecaps );
		pPlayer->TeamFortress_SetSpeed();
	}

	BaseClass::DoMeleeDamage( ent, trace );
}

//-----------------------------------------------------------------------------
float CTFBonesaw::GetBoneSawSpeedMod( void ) 
{ 
	const int MAX_HEADS_FOR_SPEED = 10;
	// Calculate Speed based on heads
	CTFPlayer *pPlayer = ToTFPlayer( GetOwnerEntity() );

	int iTakeHeads = 0;
	CALL_ATTRIB_HOOK_INT( iTakeHeads, add_head_on_hit );
	if ( pPlayer && iTakeHeads )
	{
		int iDecaps = Min( MAX_HEADS_FOR_SPEED, pPlayer->m_Shared.GetDecapitations() );
		return 1.f + (iDecaps * 0.05f);
	}
	return 1.f; 
}

//-----------------------------------------------------------------------------
int CTFBonesaw::GetCount( void )
{
	CTFPlayer *pOwner = ToTFPlayer( GetOwner() );
	if ( !pOwner )
		return 0;

	return pOwner->m_Shared.GetDecapitations();
}

#ifdef CLIENT_DLL
//-----------------------------------------------------------------------------
// Purpose: 
//-----------------------------------------------------------------------------
void CTFBonesaw::OnDataChanged( DataUpdateType_t updateType )
{
	BaseClass::OnDataChanged( updateType );

	UpdateChargePoseParam(); 
}

//-----------------------------------------------------------------------------
// Purpose: 
//-----------------------------------------------------------------------------
void CTFBonesaw::UpdateAttachmentModels( void )
{
	BaseClass::UpdateAttachmentModels();

	if ( m_hViewmodelAttachment )
	{
		m_iUberChargePoseParam = m_hViewmodelAttachment->LookupPoseParameter( m_hViewmodelAttachment->GetModelPtr(), UBERSAW_CHARGE_POSEPARAM );
	}
	else
	{
		m_iUberChargePoseParam = LookupPoseParameter( GetModelPtr(), UBERSAW_CHARGE_POSEPARAM );
	}
}

//-----------------------------------------------------------------------------
// Purpose: 
//-----------------------------------------------------------------------------
void CTFBonesaw::UpdateChargePoseParam( void )
{
	if ( m_iUberChargePoseParam >= 0 )
	{
		CTFPlayer *pTFPlayer = ToTFPlayer( GetOwner() );
		if ( pTFPlayer && pTFPlayer->IsPlayerClass( TF_CLASS_MEDIC ) )
		{
			CWeaponMedigun *pMedigun = (CWeaponMedigun *)pTFPlayer->Weapon_OwnsThisID( TF_WEAPON_MEDIGUN );
			if ( pMedigun )
			{
				m_flChargeLevel = pMedigun->GetChargeLevel();

				// On the local client, we push the pose parameters onto the attached model
				if ( m_hViewmodelAttachment )
				{
					m_hViewmodelAttachment->SetPoseParameter( m_iUberChargePoseParam, pMedigun->GetChargeLevel() );
				}
			}
		}
	}
}

//-----------------------------------------------------------------------------
// Purpose: 
//-----------------------------------------------------------------------------
void CTFBonesaw::GetPoseParameters( CStudioHdr *pStudioHdr, float poseParameter[MAXSTUDIOPOSEPARAM] )
{
	if ( !pStudioHdr )
		return;

	BaseClass::GetPoseParameters( pStudioHdr, poseParameter );

	if ( m_iUberChargePoseParam >= 0 )
	{
		poseParameter[m_iUberChargePoseParam] = m_flChargeLevel;
	}
}

#endif