import logging
import sys
import smpplib.gsm
import smpplib.client
import smpplib.consts

# if you want to know what's happening
logging.basicConfig(level='DEBUG')

client = smpplib.client.Client('localhost', 2775)

def SendSms(source, destination, content):
    # Two parts, GSM /default / UCS2, SMS with UDH
    parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(content)
    # Print when obtain message_id
    client.set_message_sent_handler(
        lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.message_id)))

    # Handle delivery receipts (and any MO SMS)
    def handle_deliver_sm(pdu):
            sys.stdout.write('delivered {}\n'.format(pdu.receipted_message_id))
            return 0 # cmd status for deliver_sm_resp

    client.set_message_received_handler(lambda pdu: handle_deliver_sm(pdu))
    #
    client.connect()
    client.bind_transceiver(system_id='test id', password='abc 123')

    for part in parts:
        pdu = client.send_message(
            source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,
            source_addr_npi=smpplib.consts.SMPP_NPI_UNK,
            # Make sure it is a byte string, not unicode:
            source_addr= source,

            dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
            dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
            # Make sure these two params are byte strings, not unicode:
            destination_addr= destination,
            short_message=part,

            data_coding=encoding_flag,
            esm_class=msg_type_flag,
            registered_delivery=True,
        )
        print(pdu.sequence)
    client.listen()
# Enters a loop, waiting for incoming PDUs
#