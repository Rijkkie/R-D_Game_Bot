#===============================================================================
# Message v1.0
# - Last Updated: 24 May 2021
#===============================================================================
# Update History
# ..............................................................................
# 24 May 2021 - Split create_winner_message from common.py. -YJ
# 24 Apr 2021 - added two extra functions maybe? -RK
#               (create_winner_message -YJ)
# 18 Apr 2021 - Started and finished common.py. -YJ
#===============================================================================
# Notes
# ..............................................................................
# - create_winner_message relies too heavily on the username being less than 16
#   characters and being purely alphanumerical. I recommend just doing a mention
#   for the username. -YJ
#===============================================================================
# Description
# ..............................................................................
# message.py contains RK's create_winner_message. Might be a good file to add
# some standard responses to in the future.
#===============================================================================

def create_winner_message(winner):
    winner_message = ":clap::regional_indicator_h::regional_indicator_a::regional_indicator_s::regional_indicator_w::regional_indicator_o::regional_indicator_n::regional_indicator_t::regional_indicator_h::regional_indicator_e::regional_indicator_g::regional_indicator_a::regional_indicator_m::regional_indicator_e::clap:"
    audience = ":clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap:"
    message_length = 15
    clap = ":clap:"
    if len(winner)>message_length:
        return audience + "\n" + winner_message + "\n" + audience
    else:
        start_position = 7
        start_position = start_position - int(len(winner)/2)
        end = 15 - start_position - len(winner)
        winner_name = ""
        for i in range(start_position):
            winner_name += clap
        winner_name += string_to_emoji(winner)
        for i in range(end):
            winner_name += clap
        return audience +"\n" +  winner_name + "\n"  + winner_message + "\n" + audience
