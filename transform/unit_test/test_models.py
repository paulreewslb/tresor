import pandas as _pd
import numpy as _np

import transform.models.models as md

def test_models():

    config = {
        'column': 'BP_ratio',
        'groupby_item': 'industry',
        'lower_percentile': 0.01,
        'upper_percentile': 0.99,
        'neutralize_item': {
            "beta": "_beta_neutralize",
            "dollar": "_dollar_neutralize"
        }
    }

    test_df = _pd.DataFrame({
        'BP_ratio': {
            0: 0.7,
            1: 1.2,
            2: 0.8,
            3: 0.6,
            4: 0.85,
            5: 0.77,
            6: 0.8,
            7: 0.55,
            8: 0.76,
            9: 0.66,
            10: 0.96,
            11: 0.2
        },
        'industry': {
            0: 'Auto',
            1: 'Auto',
            2: 'Textile',
            3: 'Textile',
            4: 'Auto',
            5: 'Auto',
            6: 'Auto',
            7: 'Auto',
            8: 'Auto',
            9: 'Auto',
            10: 'Auto',
            11: 'Auto',
        },

        'sec_id': {
            0: 'A',
            1: 'B',
            2: 'C',
            3: 'D',
            4: 'E',
            5: 'F',
            6: 'G',
            7: 'H',
            8: 'I',
            9: 'J',
            10: 'K',
            11: 'L',
        },

        'beta': {
            0: 2.0,
            1: 3.5,
            2: 0.5,
            3: -0.1,
            4: 1.5,
            5: 1.2,
            6: 4.0,
            7: 5.0,
            8: 2.3,
            9: 0.5,
            10: 0.0,
            11: 0.2,
        }
    })

    df_trimmed = md.trim_percentile(df=test_df, config=config)
    df_ranked = md.rank_and_standardize(df=df_trimmed, config=config)
    df_neutralized = md.neutralize(df=df_ranked, config=config)

    print(df_neutralized)

if __name__ == '__main__':

    test_models()