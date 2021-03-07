import pandas as pd
from vincentvanbot.visionlabels.apicall import get_labels_url


def get_labels_df(df, max_results, proba_threshold=0.6):
    """Get labels for each url of the given df."""
    list_of_dicts = []

    for i in range(len(df)):
        url = df.iloc[i]["URL"]
        labels_dict = get_labels_url(url, max_results=max_results, proba_threshold=proba_threshold)
        labels_dict['Index'] = i
        list_of_dicts.append(labels_dict)

    final_df = pd.DataFrame(list_of_dicts)
    final_df.fillna(0, inplace= True)
    final_df.set_index('Index', inplace = True)
    
    return final_df


if __name__ == '__main__':
    from vincentvanbot.data import get_data_locally
    df = get_data_locally(5)
    labels_df = get_labels_df(df,25)
    print(labels_df)