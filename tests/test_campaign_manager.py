from managers.campaign_manager import (
    CampaignManager,
    CampaignConfig,
    CampaignType,
    BiddingStrategyType,
)


class _ManualCpc:
    def __init__(self):
        self.enhanced_cpc_enabled = False


class _CampaignStub:
    def __init__(self):
        self.manual_cpc = _ManualCpc()


class _ClientStub:
    def get_type(self, _name):
        return object()


def test_set_bidding_strategy_manual_cpc_enables_enhanced_cpc():
    manager = CampaignManager(_ClientStub())
    campaign = _CampaignStub()

    config = CampaignConfig(
        name="Test Campaign",
        campaign_type=CampaignType.SEARCH,
        bidding_strategy_type=BiddingStrategyType.MANUAL_CPC,
    )

    manager._set_bidding_strategy(campaign, config)

    assert campaign.manual_cpc.enhanced_cpc_enabled is True
