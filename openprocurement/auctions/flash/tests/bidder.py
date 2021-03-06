# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.bidder import (
    AuctionBidderDocumentResourceTestMixin,
    AuctionBidderDocumentWithDSResourceTestMixin
)
from openprocurement.auctions.core.tests.blanks.bidder_blanks import (
    # AuctionBidderFeaturesResourceTest
    features_bidder_invalid
)
from openprocurement.auctions.flash.tests.base import (
    BaseAuctionWebTest, test_features_auction_data, test_organization
)
from openprocurement.auctions.flash.tests.blanks.bidder_blanks import (
    # AuctionBidderResourceTest
    create_auction_bidder_invalid,
    create_auction_bidder,
    patch_auction_bidder,
    get_auction_bidder,
    delete_auction_bidder,
    get_auction_auctioners,
    bid_Administrator_change,
    # AuctionBidderFeaturesResourceTest
    features_bidder,
    # AuctionBidderDocumentResourceTest
    create_auction_bidder_document_nopending,
)


class AuctionBidderResourceTest(BaseAuctionWebTest):
    initial_status = 'active.tendering'
    initial_organization = test_organization
    test_create_auction_bidder_invalid = snitch(create_auction_bidder_invalid)
    test_create_auction_bidder = snitch(create_auction_bidder)
    test_patch_auction_bidder = snitch(patch_auction_bidder)
    test_get_auction_bidder = snitch(get_auction_bidder)
    test_delete_auction_bidder = snitch(delete_auction_bidder)
    test_get_auction_auctioners = snitch(get_auction_auctioners)
    test_bid_Administrator_change = snitch(bid_Administrator_change)

    
class AuctionBidderFeaturesResourceTest(BaseAuctionWebTest):
    initial_data = test_features_auction_data
    initial_status = 'active.tendering'
    initial_organization = test_organization
    test_features_bidder = snitch(features_bidder)
    test_features_bidder_invalid = snitch(features_bidder_invalid)

    def test_features_bidder(self):
        test_features_bids = [
            {
                "parameters": [
                    {
                        "code": i["code"],
                        "value": 0.1,
                    }
                    for i in self.initial_data['features']
                ],
                "status": "active",
                "tenderers": [
                    test_organization
                ],
                "value": {
                    "amount": 469,
                    "currency": "UAH",
                    "valueAddedTaxIncluded": True
                }
            },
            {
                "parameters": [
                    {
                        "code": i["code"],
                        "value": 0.15,
                    }
                    for i in self.initial_data['features']
                ],
                "tenderers": [
                    test_organization
                ],
                "status": "draft",
                "value": {
                    "amount": 479,
                    "currency": "UAH",
                    "valueAddedTaxIncluded": True
                }
            }
        ]
        for i in test_features_bids:
            response = self.app.post_json('/auctions/{}/bids'.format(self.auction_id), {'data': i})
            self.assertEqual(response.status, '201 Created')
            self.assertEqual(response.content_type, 'application/json')
            bid = response.json['data']
            bid.pop(u'date')
            bid.pop(u'id')
            bid.pop(u'owner')
            self.assertEqual(bid, i)

class AuctionBidderDocumentResourceTest(BaseAuctionWebTest,
                                        AuctionBidderDocumentResourceTestMixin):
    initial_status = 'active.tendering'

    def setUp(self):
        super(AuctionBidderDocumentResourceTest, self).setUp()
        # Create bid
        response = self.app.post_json('/auctions/{}/bids'.format(
            self.auction_id), {'data': {'tenderers': [test_organization], "value": {"amount": 500}}})
        bid = response.json['data']
        self.bid_id = bid['id']
        self.bid_token = response.json['access']['token']
    test_create_auction_bidder_document_nopending = snitch(create_auction_bidder_document_nopending)

    def test_not_found(self):
        response = self.app.post('/auctions/some_id/bids/some_id/documents', status=404, upload_files=[
                                 ('file', 'name.doc', 'content')])
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'auction_id'}
        ])

class AuctionBidderDocumentWithDSResourceTest(BaseAuctionWebTest,
                                              AuctionBidderDocumentResourceTestMixin,
                                              AuctionBidderDocumentWithDSResourceTestMixin):
    initial_status = 'active.tendering'

    def setUp(self):
        super(AuctionBidderDocumentWithDSResourceTest, self).setUp()
        # Create bid
        response = self.app.post_json('/auctions/{}/bids'.format(
            self.auction_id), {'data': {'tenderers': [test_organization], "value": {"amount": 500}}})
        bid = response.json['data']
        self.bid_id = bid['id']
        self.bid_token = response.json['access']['token']
    docservice = True

    test_create_auction_bidder_document_nopending = snitch(create_auction_bidder_document_nopending)


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AuctionBidderResourceTest))
    tests.addTest(unittest.makeSuite(AuctionBidderFeaturesResourceTest))
    tests.addTest(unittest.makeSuite(AuctionBidderDocumentResourceTest))
    tests.addTest(unittest.makeSuite(AuctionBidderDocumentWithDSResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
