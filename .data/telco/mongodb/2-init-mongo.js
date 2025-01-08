
const customerPreferencesData = [
    {
        "customer_guid": "5e58b417-3cde-4cbd-b9e7-7896cf3d435b",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/adam.mcdaniel"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-10T12:00:00Z",
            "lastAppLogin": "2024-08-12T14:30:00Z"
        },
        "customerNotes": [
            {
                "author": "agent1",
                "date": "2024-08-15T09:30:00Z",
                "content": "Discussed family plan options, customer interested in upgrading."
            }
        ]
    },
    {
        "customer_guid": "859d2da9-c54d-4501-82ec-04bd3a276cd8",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {
            "twitter": "https://twitter.com/daniel.lane"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T18:45:00Z",
            "lastAppLogin": "2024-08-11T20:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent2",
                "date": "2024-08-16T11:15:00Z",
                "content": "Customer called regarding billing inquiry."
            }
        ]
    },
    {
        "customer_guid": "6d4f76b5-31b4-4018-bb54-2cdd2bd4ace6",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/nathan.moore"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-14T15:00:00Z",
            "lastAppLogin": "2024-08-16T16:30:00Z"
        },
        "customerNotes": [
            {
                "author": "agent3",
                "date": "2024-08-17T14:00:00Z",
                "content": "Customer requested information on family plans."
            }
        ]
    },
    {
        "customer_guid": "fe0d91d6-2237-4343-9b70-626997d40025",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/katherine.arellano"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-13T10:00:00Z",
            "lastAppLogin": "2024-08-14T12:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent4",
                "date": "2024-08-18T09:00:00Z",
                "content": "Customer expressed interest in high-data plans."
            }
        ]
    },
    {
        "customer_guid": "4a071173-8666-4368-bc46-ef8dd58c9406",
        "preferences": {
            "contactMethod": "SMS",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-11T08:00:00Z",
            "lastAppLogin": "2024-08-12T11:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent5",
                "date": "2024-08-17T13:00:00Z",
                "content": "Customer interested in budget-conscious plans."
            }
        ]
    },
    {
        "customer_guid": "b8b31280-c88c-44c8-8f89-66262c1b57b0",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/mark.holland"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T09:45:00Z",
            "lastAppLogin": "2024-08-10T11:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent6",
                "date": "2024-08-18T10:00:00Z",
                "content": "Customer is satisfied with current family plan."
            }
        ]
    },
    {
        "customer_guid": "dd264970-f61f-429f-97f8-4761fea4de2f",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": false
        },
        "socialMedia": {
            "twitter": "https://twitter.com/alexis.smith"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-08T18:00:00Z",
            "lastAppLogin": "2024-08-09T21:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent7",
                "date": "2024-08-17T12:00:00Z",
                "content": "Customer interested in new tech offerings."
            }
        ]
    },
    {
        "customer_guid": "d6d8dc95-2321-49f2-a86f-e5ddf50e3129",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-10T07:45:00Z",
            "lastAppLogin": "2024-08-11T08:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent8",
                "date": "2024-08-16T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "e6b467db-557a-443f-8da0-c3dcaec5663a",
        "preferences": {
            "contactMethod": "SMS",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/matthew.reed"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-15T14:00:00Z",
            "lastAppLogin": "2024-08-16T15:30:00Z"
        },
        "customerNotes": [
            {
                "author": "agent9",
                "date": "2024-08-17T11:00:00Z",
                "content": "Customer inquired about frequent traveler perks."
            }
        ]
    },
    {
        "customer_guid": "3afe9e44-7e01-4d8c-a610-ddac5662396d",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "linkedin": "https://linkedin.com/in/isaac.kramer"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-11T12:00:00Z",
            "lastAppLogin": "2024-08-13T14:30:00Z"
        },
        "customerNotes": [
            {
                "author": "agent10",
                "date": "2024-08-17T10:30:00Z",
                "content": "Customer is looking into new tech offerings."
            }
        ]
    },
    {
        "customer_guid": "2e8dd6e8-cc7d-4bd7-ba52-ce7ae20bc0c6",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T11:45:00Z",
            "lastAppLogin": "2024-08-10T13:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent11",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "2373100d-630d-41fe-93dd-1134dbbe7e0e",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/christopher.davis"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-13T13:30:00Z",
            "lastAppLogin": "2024-08-15T14:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent12",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer interested in high-data plans."
            }
        ]
    },
    {
        "customer_guid": "c2646b8f-6f3d-4b91-a8ae-b5a47073f997",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": false
        },
        "socialMedia": {
            "twitter": "https://twitter.com/samantha.anderson"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-14T09:00:00Z",
            "lastAppLogin": "2024-08-15T11:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent13",
                "date": "2024-08-17T13:30:00Z",
                "content": "Customer is interested in tech-savvy offerings."
            }
        ]
    },
    {
        "customer_guid": "adff1f8e-e518-4ea6-80ca-c9ac9c7a5c33",
        "preferences": {
            "contactMethod": "SMS",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-11T10:45:00Z",
            "lastAppLogin": "2024-08-12T12:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent14",
                "date": "2024-08-17T15:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "5e609951-4c6d-47b8-8d25-d6f73ab1032b",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/james.goodman"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-12T11:00:00Z",
            "lastAppLogin": "2024-08-14T13:30:00Z"
        },
        "customerNotes": [
            {
                "author": "agent15",
                "date": "2024-08-17T14:00:00Z",
                "content": "Customer is looking into high-data plans."
            }
        ]
    },
    {
        "customer_guid": "1a284372-b632-491a-95e9-fff159a76d21",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": true
        },
        "socialMedia": {
            "linkedin": "https://linkedin.com/in/jeremy.washington"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-10T15:30:00Z",
            "lastAppLogin": "2024-08-11T16:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent16",
                "date": "2024-08-18T08:30:00Z",
                "content": "Customer interested in tech-savvy plans."
            }
        ]
    },
    {
        "customer_guid": "b2570f3f-8f2e-4f2b-a82f-00da213f68bc",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-11T09:45:00Z",
            "lastAppLogin": "2024-08-12T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent17",
                "date": "2024-08-17T12:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "1ec159cd-1e5b-4519-8a15-233fb6badd4d",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/jessica.sharp"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-13T12:00:00Z",
            "lastAppLogin": "2024-08-14T13:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent18",
                "date": "2024-08-18T10:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "250de58a-17b3-4aad-96e5-21b8028f2da2",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": false
        },
        "socialMedia": {
            "twitter": "https://twitter.com/amanda.norton"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:45:00Z",
            "lastAppLogin": "2024-08-10T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent19",
                "date": "2024-08-17T11:30:00Z",
                "content": "Customer interested in tech-savvy plans."
            }
        ]
    },
    {
        "customer_guid": "a9e2c82b-cbb3-48a0-88e2-8c4c370e727c",
        "preferences": {
            "contactMethod": "SMS",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-12T13:45:00Z",
            "lastAppLogin": "2024-08-13T14:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent20",
                "date": "2024-08-17T13:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "3f711a10-53ac-4609-b061-c4d6ae5cd2d6",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/crystal.parker"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-11T14:00:00Z",
            "lastAppLogin": "2024-08-12T15:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent21",
                "date": "2024-08-18T09:00:00Z",
                "content": "Customer is looking into high-data plans."
            }
        ]
    },
    {
        "customer_guid": "eadeab1b-eb46-4257-9680-62a4e846ff56",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {
            "linkedin": "https://linkedin.com/in/ricky.dudley"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-10T11:30:00Z",
            "lastAppLogin": "2024-08-11T12:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent22",
                "date": "2024-08-17T08:30:00Z",
                "content": "Customer interested in tech-savvy plans."
            }
        ]
    },
    {
        "customer_guid": "bea981be-622c-47dc-b06e-f93e7f6fcc8c",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T07:45:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent23",
                "date": "2024-08-17T14:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "cdf887b8-8fd0-4fe1-b3b0-857792813f3d",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/andrea.smith"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-12T11:30:00Z",
            "lastAppLogin": "2024-08-13T12:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent24",
                "date": "2024-08-18T10:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "56f07f91-10ad-45ab-a0bb-3133f125a669",
        "preferences": {
            "contactMethod": "SMS",
            "marketingOptIn": true
        },
        "socialMedia": {
            "twitter": "https://twitter.com/brandon.haley"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-08T18:00:00Z",
            "lastAppLogin": "2024-08-09T19:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent25",
                "date": "2024-08-17T11:00:00Z",
                "content": "Customer is interested in tech-savvy offerings."
            }
        ]
    },
    {
        "customer_guid": "b1b77625-4046-4753-8dac-52d95248aee7",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T09:00:00Z",
            "lastAppLogin": "2024-08-10T10:30:00Z"
        },
        "customerNotes": [
            {
                "author": "agent26",
                "date": "2024-08-17T12:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "83a58359-c018-4190-90ca-459d0794ebdb",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/timothy.sims"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-11T14:30:00Z",
            "lastAppLogin": "2024-08-13T15:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent27",
                "date": "2024-08-18T09:00:00Z",
                "content": "Customer interested in high-data plans."
            }
        ]
    },
    {
        "customer_guid": "60843adc-b408-4146-b75a-120a53ebe69c",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-10T10:15:00Z",
            "lastAppLogin": "2024-08-11T11:30:00Z"
        },
        "customerNotes": [
            {
                "author": "agent28",
                "date": "2024-08-17T13:30:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "d5f16f1a-a4d3-4775-bf8d-54a7537c1af7",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/christy.carter"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-12T09:00:00Z",
            "lastAppLogin": "2024-08-13T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent29",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer interested in high-data plans."
            }
        ]
    },
    {
        "customer_guid": "1969bbcb-d9bf-43db-b849-f31969a5391c",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": true
        },
        "socialMedia": {
            "twitter": "https://twitter.com/kristen.wright"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-14T08:30:00Z",
            "lastAppLogin": "2024-08-15T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent30",
                "date": "2024-08-17T10:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "e213281b-339d-403c-aaae-e925e19d4da9",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": false
        },
        "socialMedia": {
            "linkedin": "https://linkedin.com/in/darryl.lane"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-10T09:45:00Z",
            "lastAppLogin": "2024-08-11T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent31",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer interested in tech-savvy plans."
            }
        ]
    },
    {
        "customer_guid": "c09ea3a3-a7e9-46cd-bfb7-9a2bedc95cc2",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:30:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent32",
                "date": "2024-08-17T10:30:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "fb6e1f6b-6eb0-4e43-bef0-412fae682158",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/gabriel.campbell"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-12T11:00:00Z",
            "lastAppLogin": "2024-08-14T12:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent33",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "3ce95a8e-0775-4c74-a76c-c0d4b1d9169e",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": false
        },
        "socialMedia": {
            "twitter": "https://twitter.com/linda.johnson"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-10T09:00:00Z",
            "lastAppLogin": "2024-08-11T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent34",
                "date": "2024-08-17T11:00:00Z",
                "content": "Customer interested in tech-savvy plans."
            }
        ]
    },
    {
        "customer_guid": "cba3ab69-fac8-4094-a271-38d6a9600bac",
        "preferences": {
            "contactMethod": "SMS",
            "marketingOptIn": true
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-11T10:15:00Z",
            "lastAppLogin": "2024-08-12T11:30:00Z"
        },
        "customerNotes": [
            {
                "author": "agent35",
                "date": "2024-08-17T12:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "ede031dc-6370-4307-bb7b-375187141ee3",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/sharon.santiago"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-13T09:45:00Z",
            "lastAppLogin": "2024-08-14T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent36",
                "date": "2024-08-18T08:30:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "cc611e70-8af8-4315-a35a-69198e35c526",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-10T08:30:00Z",
            "lastAppLogin": "2024-08-11T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent37",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "a2f97322-bc51-46ed-a14f-c0c587151796",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/wesley.woodard"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-12T09:00:00Z",
            "lastAppLogin": "2024-08-13T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent38",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer interested in high-data plans."
            }
        ]
    },
    {
        "customer_guid": "3d4da6a7-ff85-4eb1-955e-61beb017c170",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": false
        },
        "socialMedia": {
            "linkedin": "https://linkedin.com/in/robert.brown"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent39",
                "date": "2024-08-17T10:00:00Z",
                "content": "Customer interested in tech-savvy plans."
            }
        ]
    },
    {
        "customer_guid": "cdb74bc6-00f7-4cf7-8d42-527238afe3a2",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T09:45:00Z",
            "lastAppLogin": "2024-08-10T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent40",
                "date": "2024-08-17T11:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "2d553286-835f-4404-804d-d281e0d4a0b6",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/cynthia.henderson"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-13T08:45:00Z",
            "lastAppLogin": "2024-08-14T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent41",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "928d1630-2258-49f4-8821-f5b1f3ac40ea",
        "preferences": {
            "contactMethod": "SMS",
            "marketingOptIn": true
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-11T10:15:00Z",
            "lastAppLogin": "2024-08-12T11:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent42",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "59898f71-c9c9-48f4-8104-ad62b7b441b2",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/ashley.martin"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-14T08:30:00Z",
            "lastAppLogin": "2024-08-15T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent43",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer interested in tech-savvy plans."
            }
        ]
    },
    {
        "customer_guid": "2a5c829c-dbed-415d-bd77-59029fb9c0f5",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T10:30:00Z",
            "lastAppLogin": "2024-08-10T11:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent44",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "47e9397f-3af9-466b-9513-9b40d5ef027f",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/samantha.jones"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-12T11:30:00Z",
            "lastAppLogin": "2024-08-14T13:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent45",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "3a4f0839-310a-440f-b6d8-748c934d7cec",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "twitter": "https://twitter.com/kristy.cain"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-10T09:30:00Z",
            "lastAppLogin": "2024-08-11T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent46",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer interested in tech-savvy plans."
            }
        ]
    },
    {
        "customer_guid": "eb783b09-7997-424a-869c-210e58e38d91",
        "preferences": {
            "contactMethod": "SMS",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent47",
                "date": "2024-08-17T10:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "54350f41-ad97-40f4-8161-6e9a628a0df7",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/rachel.alvarado"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-14T09:30:00Z",
            "lastAppLogin": "2024-08-15T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent48",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "8c418e68-48aa-411b-8ced-21984fe9db6d",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:45:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent49",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "98cc225f-1ade-4936-af64-701183f4eeaf",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/samantha.torres"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-12T09:00:00Z",
            "lastAppLogin": "2024-08-13T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent50",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer interested in high-data plans."
            }
        ]
    },
    {
        "customer_guid": "13e68987-db07-423c-b1f8-69fbc461658e",
        "preferences": {
            "contactMethod": "SMS",
            "marketingOptIn": true
        },
        "socialMedia": {
            "twitter": "https://twitter.com/samuel.barrera"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-10T09:30:00Z",
            "lastAppLogin": "2024-08-11T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent51",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer interested in tech-savvy plans."
            }
        ]
    },
    {
        "customer_guid": "1ba53ec7-c99d-46b6-80e8-8650c4696ba1",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent52",
                "date": "2024-08-17T10:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "fdf4cba8-4c47-4038-9515-e61360a666ed",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/mike.williams"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-14T09:30:00Z",
            "lastAppLogin": "2024-08-15T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent53",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "d83da028-a09b-4b4b-bde2-fec4af6a31b0",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent54",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "ce396a23-10e2-4252-b756-685308207bf1",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/kevin.shaw"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-13T09:45:00Z",
            "lastAppLogin": "2024-08-14T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent55",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer interested in tech-savvy plans."
            }
        ]
    },
    {
        "customer_guid": "361986fa-123f-4817-aa16-3f6b8ae368a2",
        "preferences": {
            "contactMethod": "SMS",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent56",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "03775cc7-9186-45ef-a090-ba6fc711fb81",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/shaun.clark"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-14T09:30:00Z",
            "lastAppLogin": "2024-08-15T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent57",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "1f8d6822-8b51-452f-8a80-f4d03d01384e",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": false
        },
        "socialMedia": {
            "linkedin": "https://linkedin.com/in/veronica.peters"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent58",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer interested in tech-savvy plans."
            }
        ]
    },
    {
        "customer_guid": "d35250ee-1615-4490-aabc-32cfec3c43f3",
        "preferences": {
            "contactMethod": "SMS",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent59",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "838f7882-b114-42ce-98e3-1c9facaf4835",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/mark.mcguire"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-13T09:30:00Z",
            "lastAppLogin": "2024-08-14T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent60",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "6d363273-8278-4013-9f7e-e8da036e634a",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": true
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-10T08:00:00Z",
            "lastAppLogin": "2024-08-11T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent61",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "41f8b31e-a172-4b68-8148-a0d350998c03",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/nicole.powell"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-14T09:30:00Z",
            "lastAppLogin": "2024-08-15T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent62",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "1d8576dd-a741-4c55-828f-90154dce55fd",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent63",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "eb36ad5b-f6ab-4c18-a180-4f0f8f4964c5",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/jessica.weber"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-13T09:45:00Z",
            "lastAppLogin": "2024-08-14T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent64",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "8e616e1c-e514-484d-bddc-5296e3fde187",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent65",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "e2304b5c-15b5-4d84-aec6-fdef4d6bb3d2",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/eileen.johnson"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-12T09:00:00Z",
            "lastAppLogin": "2024-08-14T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent66",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "f46eed39-eeff-4d80-b6d2-9849226c6816",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent67",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "bc024054-49fa-45c4-90fd-3a44980fdf78",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/nicole.kramer"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-13T09:30:00Z",
            "lastAppLogin": "2024-08-14T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent68",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "c4eb8d4c-d28d-4bbf-b2af-a72c97cfccb6",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent69",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "3ebc550d-c14b-4a18-9dad-2fa328063486",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/joseph.nelson"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-13T09:30:00Z",
            "lastAppLogin": "2024-08-14T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent70",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "f1a5ea36-30c6-4d0e-99ab-c9578ff321ce",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent71",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "beceb10a-a2a4-4ba3-a7ec-202724124330",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/marie.johnson"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-12T09:00:00Z",
            "lastAppLogin": "2024-08-14T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent72",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "d97d5a32-ac0a-45d3-8baf-bb3b24a4f1f6",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent73",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "55bb9264-3230-421c-b249-3e299d4de9d7",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/james.barnes"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-13T09:30:00Z",
            "lastAppLogin": "2024-08-14T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent74",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "1da7707e-d1a1-4989-a104-aae364d2f9b7",
        "preferences": {
            "contactMethod": "SMS",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent75",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "96dbde7a-aa94-466e-9480-666220398fff",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/dale.thompson"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-14T09:30:00Z",
            "lastAppLogin": "2024-08-15T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent76",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "a4008bd3-cd15-4581-944e-c2e003ce6da4",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent77",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "c32f754b-ef6c-4140-aa96-4736b1d0739d",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/jacqueline.gonzalez"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-14T09:30:00Z",
            "lastAppLogin": "2024-08-15T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent78",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "aee7a5f0-0b6a-46c8-968f-49a087e69e58",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent79",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "f7c7820a-fefc-4ecc-b120-5f0869cbf4cc",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/steven.adams"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-14T09:30:00Z",
            "lastAppLogin": "2024-08-15T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent80",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "fb58ecf7-c670-4729-bec2-9b5eb877c5d9",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent81",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "825cd363-053e-4f6e-b7c3-7c3cb3d7336c",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/todd.valdez"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-14T09:30:00Z",
            "lastAppLogin": "2024-08-15T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent82",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "fabe9a77-cc2d-43bb-93e4-0f5d90aaf077",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent83",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "db2f7e4a-6682-4ba2-9568-edb2a005d543",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/jenny.roberts"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-13T09:30:00Z",
            "lastAppLogin": "2024-08-14T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent84",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "f995b872-6bbb-4553-aebd-5e8a241b05af",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent85",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "1bdfcbdb-b9d2-4a55-9dfb-cb1e8afc245d",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/leonard.campbell"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-14T09:30:00Z",
            "lastAppLogin": "2024-08-15T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent86",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "db8b20a0-e387-4c5b-bb63-ce5467edcf91",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent87",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "27d71eb9-250f-4130-9485-fdf8ace8bb3e",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/samuel.montgomery"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-14T09:30:00Z",
            "lastAppLogin": "2024-08-15T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent88",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "d562c9e4-1415-465e-b0c5-1ccfe1032832",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent89",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "087d4d2a-1f7b-461c-b13c-ab55c79cb4d4",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/elizabeth.mccoy"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-13T09:30:00Z",
            "lastAppLogin": "2024-08-14T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent90",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "38745d1f-3200-49a8-bc0e-b5ba34f98152",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent91",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "11798e10-aa49-4c28-8075-eac791ca1a8f",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/david.bruce"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-13T09:30:00Z",
            "lastAppLogin": "2024-08-14T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent92",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "285e3e2b-9d48-479a-9528-c46dc59b6e2e",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent93",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "b5a20328-6237-4bdc-b2b0-bc5496bac4b1",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/jessica.moore"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-14T09:30:00Z",
            "lastAppLogin": "2024-08-15T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent94",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "7b0dcbb9-1291-4bdd-aa24-2a3fa2faa51b",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent95",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "ee4006c8-1bd9-421a-af88-1828ab96e6b5",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/amanda.coleman"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-13T09:30:00Z",
            "lastAppLogin": "2024-08-14T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent96",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "536aadf0-1098-487c-9a63-5fe623591da7",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent97",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "130dce11-b01f-4e0e-82e0-c7fc00922225",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/marissa.montoya"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-13T09:30:00Z",
            "lastAppLogin": "2024-08-14T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent98",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    },
    {
        "customer_guid": "31750099-435b-46c8-9271-1c30fd70d156",
        "preferences": {
            "contactMethod": "phone",
            "marketingOptIn": false
        },
        "socialMedia": {},
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-09T08:00:00Z",
            "lastAppLogin": "2024-08-10T09:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent99",
                "date": "2024-08-17T09:00:00Z",
                "content": "Customer prefers budget-friendly plans."
            }
        ]
    },
    {
        "customer_guid": "cc52ba76-6236-4c5b-b999-93fd74194c7d",
        "preferences": {
            "contactMethod": "email",
            "marketingOptIn": true
        },
        "socialMedia": {
            "facebook": "https://facebook.com/jessica.moreno"
        },
        "behavioralData": {
            "lastWebsiteVisit": "2024-08-14T09:30:00Z",
            "lastAppLogin": "2024-08-15T10:00:00Z"
        },
        "customerNotes": [
            {
                "author": "agent100",
                "date": "2024-08-18T08:00:00Z",
                "content": "Customer is exploring high-data plans."
            }
        ]
    }
];

db.createCollection("customerPreferences", {
    validator: {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["customer_guid", "preferences", "behavioralData", "customerNotes"],
            "properties": {
                "customer_guid": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "preferences": {
                    "bsonType": "object",
                    "required": ["contactMethod", "marketingOptIn"],
                    "properties": {
                        "contactMethod": {
                            "bsonType": "string",
                            "enum": ["email", "phone", "SMS"],
                            "description": "must be one of 'email', 'phone', or 'SMS' and is required"
                        },
                        "marketingOptIn": {
                            "bsonType": "bool",
                            "description": "must be a boolean value and is required"
                        }
                    }
                },
                "socialMedia": {
                    "bsonType": "object",
                    "properties": {
                        "facebook": {
                            "bsonType": "string",
                            "pattern": "^(https?:\\/\\/)?(www\\.)?facebook.com\\/.*$",
                            "description": "must be a valid Facebook URL"
                        },
                        "twitter": {
                            "bsonType": "string",
                            "pattern": "^(https?:\\/\\/)?(www\\.)?twitter.com\\/.*$",
                            "description": "must be a valid Twitter URL"
                        },
                        "linkedin": {
                            "bsonType": "string",
                            "pattern": "^(https?:\\/\\/)?(www\\.)?linkedin.com\\/.*$",
                            "description": "must be a valid LinkedIn URL"
                        }
                    },
                    "description": "socialMedia is an object containing social media profile URLs"
                },
                "behavioralData": {
                    "bsonType": "object",
                    "required": ["lastWebsiteVisit", "lastAppLogin"],
                    "properties": {
                        "lastWebsiteVisit": {
                            "bsonType": "string",
                            "description": "must be a valid ISO date and is required"
                        },
                        "lastAppLogin": {
                            "bsonType": "string",
                            "description": "must be a valid ISO date and is required"
                        }
                    },
                    "description": "behavioralData is an object containing behavioral metrics"
                },
                "customerNotes": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "required": ["author", "date", "content"],
                        "properties": {
                            "author": {
                                "bsonType": "string",
                                "description": "must be a string and is required"
                            },
                            "date": {
                                "bsonType": "string",
                                "description": "must be a valid ISO date and is required"
                            },
                            "content": {
                                "bsonType": "string",
                                "description": "must be a string and is required"
                            }
                        }
                    },
                    "description": "customerNotes is an array of note objects with author, date, and content"
                }
            }
        }
    }
})
db.getSiblingDB(process.env.MONGO_INITDB_DATABASE).customerPreferences.insertMany(customerPreferencesData);
