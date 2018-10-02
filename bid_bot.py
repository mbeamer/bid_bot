''' Bid Bot application for parsing bids from Everquest logs '''
import re
import sys
import argparse
from libs.lib_log_parser import LogParser
from forms.form_bid_main import bid_bot_main

raider_dict = {}
member_dict = {}
bid_array = []
bidding = None

def argparser(argv):
    ''' parse input arguments into usable form '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--eqlog", required=True, type=str, help="Path to EQ Log.")
    parser.add_argument("--rate", required=False, default=5, type=int, help="Log file sample rate.")

    return parser.parse_args(argv)

def bid_updater(new_bids):
    ''' New bids for the system '''
    for bid in new_bids:

        # - Original style bid handling - 
        # [Sun Sep 30 12:14:39 2018] Sofy tells you, '23 member'
        #
        match = re.search("\[.*\] (.*) tells you, '([0-9]+) (.*)", bid)
        if match:
            global bid_array
            bid_array.append({'player': match.group(1), 'bid': match.group(2), 'rank': match.group(3)})
            print("bid_updater: {} - {} | {} | {}".format(
                bid, 
                match.group(1), 
                match.group(2), 
                match.group(3)), flush=True)

            lbx = bidding.get_bids_box()
            winner_list = []
            lbx.Update(values=sorted(bid_array, key = lambda i:(i['rank'], i['bid']), reverse=True))

def main(eqlog, rate):
    ''' Setup and run the Bid Bot UI '''

    log_parser = LogParser(bid_updater)
    log_parser.log_filename = eqlog
    log_parser.sample_interval = rate
    global bidding
    bidding = bid_bot_main(log_parser)
    bidding.main_form()

    return 0

if __name__ == "__main__":
    # execute only if run as a script
    ARGS = argparser(sys.argv[1:])
    sys.exit(main(ARGS.eqlog, ARGS.rate))
