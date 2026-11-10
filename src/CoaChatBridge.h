/*
 * CoaChatBridge.h - the bridge between the chat modules of a Conquest of Azeroth server.
 *
 * The same file is in mod-ollama-chat-coa, mod-playerbots-auctions and mod-playerbots-immersion. None of them
 * needs another: each function below is an inline function with a static inside, so the modules that are built
 * share one of each, and a module that is not there simply leaves its part empty. Keep the copies identical.
 *
 * World thread only: register at startup, call from the world thread.
 */

#ifndef COA_CHAT_BRIDGE_H
#define COA_CHAT_BRIDGE_H

#include <cstdint>
#include <functional>
#include <string>
#include <vector>

class Player;

namespace CoaChatBridge
{
    // How a line goes out.
    enum Channel : uint8_t
    {
        CHANNEL_WHISPER = 0,    // to `to`
        CHANNEL_SAY     = 1,
        CHANNEL_YELL    = 2
    };

    // What the voice may change.
    enum Mode : uint8_t
    {
        MODE_EXACT = 0,         // the same message in the bot's own words: every number, item and place stays
        MODE_FREE  = 1          // the line is only an example of what the bot would say here
    };

    // A module with a line for a bot to say hands it to the voice (the language model of mod-ollama-chat-coa),
    // which says it in the bot's own words a few seconds later. False when there is no voice or it cannot take the
    // line now: then the module says the line itself, as it always did. `context` says what is going on, in a
    // sentence ("You are selling to Chris at the auction house."), or is empty.
    using VoiceFn = std::function<bool(Player* bot, Player* to, std::string const& line, uint8_t channel,
                                       uint8_t mode, std::string const& context)>;
    inline VoiceFn& Voice()
    {
        static VoiceFn fn;
        return fn;
    }

    inline bool Speak(Player* bot, Player* to, std::string const& line, uint8_t channel, uint8_t mode,
                      std::string const& context = std::string())
    {
        VoiceFn& fn = Voice();
        return fn && fn(bot, to, line, channel, mode, context);
    }

    // Who a bot is right now, as far as a module knows: "You are a beggar in Stormwind ...". The voice asks every
    // registered module and puts what they say into the bot's picture of itself. "" when the module has nothing.
    using PersonaFn = std::function<std::string(Player* bot)>;
    inline std::vector<PersonaFn>& Personas()
    {
        static std::vector<PersonaFn> fns;
        return fns;
    }

    // Something a bot went through with a person, for its memory: `what` in the second person, past tense ("You
    // sold Chris 20 Linen Cloth for 1g 20s."). `importance` 1 (trivial) to 10 (defining); `bond` how much it
    // changes what the bot thinks of the person, -10 to +10.
    using ExperienceFn = std::function<void(Player* bot, Player* with, std::string const& what, uint8_t importance,
                                            int8_t bond)>;
    inline ExperienceFn& Experience()
    {
        static ExperienceFn fn;
        return fn;
    }

    inline void Remember(Player* bot, Player* with, std::string const& what, uint8_t importance, int8_t bond)
    {
        ExperienceFn& fn = Experience();
        if (fn)
            fn(bot, with, what, importance, bond);
    }
}

#endif
