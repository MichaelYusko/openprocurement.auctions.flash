# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import opresource
from openprocurement.auctions.core.views.mixins import AuctionBidResource


@opresource(name='belowThreshold:Auction Bids',
            collection_path='/auctions/{auction_id}/bids',
            path='/auctions/{auction_id}/bids/{bid_id}',
            auctionsprocurementMethodType="belowThreshold",
            description="Auction bids")
class AuctionBidResource(AuctionBidResource):
    pass
