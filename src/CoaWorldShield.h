/*
 * CoaWorldShield.h - keeps CoA World's events (invasions, resource rushes, capital raids, Density ...) of
 * Zyth45's mod-playerbots away from our residents, and us away from the bots those events borrowed.
 * Without that mod-playerbots branch every function is empty. World thread only.
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

#ifndef COA_WORLD_SHIELD_H
#define COA_WORLD_SHIELD_H

#include "ObjectGuid.h"
#include "Player.h"
#include "RandomPlayerbotMgr.h"

#if __has_include("CoaWorldBots.h")
#include "CoaWorldBots.h"
#define LIFE_COA_WORLD 1
#endif

namespace PlayerbotsLife::CoaShield
{
#ifdef LIFE_COA_WORLD
    // Far above CoA World's own owner ids (100 ... 1000 + run id).
    constexpr uint32 Owner = 0x7E11FE00;

    inline ObjectGuid& Target()
    {
        static ObjectGuid target;
        return target;
    }

    inline bool IsTarget(Player* bot) { return bot->GetGUID() == Target(); }

    // A random bot our candidate checks let through but CoA World calls busy is one of its events' bots.
    inline bool TakenByCoaWorld(Player* bot)
    {
        return bot && sRandomPlayerbotMgr.IsRandomBot(bot) && !bot->GetGroup() && !CoaWorld::IsFreeBot(bot);
    }

    // Borrowed where it stands (far + holdFar, no teleport): CoA World leaves it alone and moves nothing.
    inline void Claim(Player* bot)
    {
        if (!bot || !sRandomPlayerbotMgr.IsRandomBot(bot) || !CoaWorld::IsFreeBot(bot))
            return;
        CoaWorld::BorrowRequest request;
        request.mapId = 0xFFFFFFFF;
        request.count = 1;
        request.nearRadius = 0.0f;
        request.teleport = false;
        request.holdFar = true;
        request.filter = &IsTarget;
        Target() = bot->GetGUID();
        CoaWorld::BorrowBots(Owner, request);
        Target().Clear();
    }

    inline void Unclaim(uint32 guidLow)
    {
        CoaWorld::ForgetBot(Owner, ObjectGuid::Create<HighGuid::Player>(guidLow));
    }
#else
    inline bool TakenByCoaWorld(Player*) { return false; }
    inline void Claim(Player*) {}
    inline void Unclaim(uint32) {}
#endif
}

#endif
