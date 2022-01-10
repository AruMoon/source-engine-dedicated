//========= Copyright Valve Corporation, All rights reserved. ============//
//
// Purpose: TF's custom C_PlayerResource
//
// $NoKeywords: $
//=============================================================================//

#ifndef C_TF_PLAYERRESOURCE_H
#define C_TF_PLAYERRESOURCE_H
#ifdef _WIN32
#pragma once
#endif

#include "tf_shareddefs.h"
#include "c_playerresource.h"
#include "tf_player_shared.h"

class C_TF_PlayerResource : public C_PlayerResource
{
	DECLARE_CLASS( C_TF_PlayerResource, C_PlayerResource );
public:
	DECLARE_CLIENTCLASS();

	C_TF_PlayerResource();
	virtual ~C_TF_PlayerResource();

	virtual int	GetTeam( int index ) OVERRIDE;

	int	GetTotalScore( int iIndex ) { return GetArrayValue( iIndex, m_iTotalScore, 0 ); }
	int GetMaxHealth( int iIndex )   { return GetArrayValue( iIndex, m_iMaxHealth, TF_HEALTH_UNDEFINED ); }
	int GetMaxHealthForBuffing( int iIndex )   { return GetArrayValue( iIndex, m_iMaxBuffedHealth, TF_HEALTH_UNDEFINED ); }
	int GetPlayerClass( int iIndex ) { return GetArrayValue( iIndex, m_iPlayerClass, TF_CLASS_UNDEFINED ); }
	int	GetActiveDominations( int iIndex ) { return GetArrayValue( iIndex, m_iActiveDominations, 0 ); }
	float GetNextRespawnTime( int iIndex ) { return (IsConnected(iIndex) ? m_flNextRespawnTime[iIndex] : 0); }
	int GetChargeLevel( int iIndex ) { return GetArrayValue( iIndex, m_iChargeLevel, 0 ); }
	int GetDamage( unsigned int nIndex );
	int GetDamageAssist( unsigned int nIndex );
	int GetDamageBoss( unsigned int nIndex );
	int GetHealing( unsigned int nIndex );
	int GetHealingAssist( unsigned int nIndex );
	int GetDamageBlocked( unsigned int nIndex );
	int GetCurrencyCollected( unsigned int nIndex );
	int GetBonusPoints( unsigned int nIndex );
	int	GetPlayerLevel( unsigned int nIndex ) { return GetArrayValue( nIndex, m_iPlayerLevel, 0 ); }
	int GetStreak( unsigned int nIndex, CTFPlayerShared::ETFStreak streak_type );
	int GetNumRespecCredits( uint32 unIndex );
	int GetNumBuybackCredits( uint32 unIndex );

	void UpdatePlayerScoreStats( void );
	void ResetPlayerScoreStats( int playerIndex = -1 );

	bool IsArenaSpectator( int iIndex ) 
	{
		if ( !IsConnected( iIndex ) )
		{
			return false;
		}
		return m_bArenaSpectator[iIndex];
	}

	int GetCountForPlayerClass( int iTeam, int iClass, bool bExcludeLocalPlayer = false );

	int GetNumPlayersForTeam( int iTeam, bool bAliveOnly );

	bool HasPremadeParties(){ return ( ( m_iPartyLeaderRedTeamIndex > 0 ) && ( m_iPartyLeaderBlueTeamIndex > 0 ) ); }
	int GetPartyLeaderRedTeamIndex(){ return m_iPartyLeaderRedTeamIndex; }
	int GetPartyLeaderBlueTeamIndex(){ return m_iPartyLeaderBlueTeamIndex; }
	int GetEventTeamStatus() { return m_iEventTeamStatus; }

	int GetPlayerClassWhenKilled( int iIndex ) { return GetArrayValue( iIndex, m_iPlayerClassWhenKilled, TF_CLASS_UNDEFINED ); }

	MM_PlayerConnectionState_t GetPlayerConnectionState( int iIndex ) const;
	
protected:
	int GetArrayValue( int iIndex, int *pArray, int defaultVal );

	int		m_iTotalScore[MAX_PLAYERS+1];
	int		m_iMaxHealth[MAX_PLAYERS+1];
	// !! This is actually m_iMaxHealthForBuffing, but we can't fix it now because of demos :-/
	int		m_iMaxBuffedHealth[MAX_PLAYERS+1];
	int		m_iPlayerClass[MAX_PLAYERS+1];
	bool	m_bArenaSpectator[MAX_PLAYERS+1];
	int		m_iActiveDominations[MAX_PLAYERS+1];

	// These variables are only networked in tournament mode
	float	m_flNextRespawnTime[MAX_PLAYERS+1];
	int		m_iChargeLevel[MAX_PLAYERS+1];

private:
	int		m_iDamage[MAX_PLAYERS+1];
	int		m_iDamageAssist[MAX_PLAYERS+1];
	int		m_iDamageBoss[MAX_PLAYERS+1];
	int		m_iHealing[MAX_PLAYERS+1];
	int		m_iHealingAssist[MAX_PLAYERS+1];
	int		m_iDamageBlocked[MAX_PLAYERS+1];
	int		m_iCurrencyCollected[MAX_PLAYERS+1];
	int		m_iBonusPoints[MAX_PLAYERS+1];
	int		m_iPlayerLevel[MAX_PLAYERS+1];
	// Pseudo multidimensional array [MAX_PLAYERS + 1][CTFPlayerShared::kTFStreak_COUNT]
	int		m_iStreaks[(MAX_PLAYERS+1) * CTFPlayerShared::kTFStreak_COUNT];
	int		m_iUpgradeRefundCredits[MAX_PLAYERS + 1];
	int		m_iBuybackCredits[MAX_PLAYERS + 1];

	int		m_iPartyLeaderBlueTeamIndex;
	int		m_iPartyLeaderRedTeamIndex;
	int		m_iEventTeamStatus;

	int		m_iPlayerClassWhenKilled[MAX_PLAYERS+1];
	MM_PlayerConnectionState_t	m_iConnectionState[MAX_PLAYERS+1];

	struct PlayerScoreboardStats_t
	{
		int	m_iPrevDamage;
		int	m_iPrevDamageAssist;
		int	m_iPrevDamageBoss;
		int	m_iPrevHealing;
		int	m_iPrevHealingAssist;
		int m_iPrevDamageBlocked;
		int	m_iPrevCurrencyCollected;
		int	m_iPrevBonusPoints;
	};

	PlayerScoreboardStats_t m_aPlayerScoreStats[MAX_PLAYERS+1];
};

extern C_TF_PlayerResource *g_TF_PR;

#endif // C_TF_PLAYERRESOURCE_H
