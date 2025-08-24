import pandas as pd
shark_pitch = pd.read_csv("/Users/jonathanzhu/Documents/Shark Tank Predictor/Training_Data & Labels/Shark_Tank_Train.csv")
shark_pitch_labels = pd.read_csv("/Users/jonathanzhu/Documents/Shark Tank Predictor/Training_Data & Labels/Sharktank_labels.csv")
shark_pitch_val = pd.read_csv("/Users/jonathanzhu/Documents/Shark Tank Predictor/Validation_Data & Labels/SharkTankValidation.csv")
shark_pitch_val_labels = pd.read_csv("/Users/jonathanzhu/Documents/Shark Tank Predictor/Validation_Data & Labels/Validation_Labels.csv")

 

#normalizing data

# Converting CSV into Library (Location attribute "Title")

def lib_convert_knn_ready_labels (csv_file_labels, title_col = "Title"):
    csv_copy = csv_file_labels.copy()
    csv_copy.set_index(title_col, inplace = True)
    csv_file_labels_lib = csv_copy.to_dict(orient = "index")
    labels_data = {}
    for title, attrs in csv_file_labels_lib.items():
        numeric_values = [attrs['Shark_deals']]
        labels_data[title] = numeric_values
    return labels_data
    

def lib_convert_knn_ready (csv_file, title_col = "Title"):
    csv_copy = csv_file.copy()
    csv_copy.set_index(title_col, inplace = True)
    csv_file_lib = csv_copy.to_dict(orient = "index")

    #Converting dictionary into KNN usable

    knn_data = {}
    for title, attrs in csv_file_lib.items():
        numeric_values = [attrs['Market_Value'], 
                        attrs['Total_Revenu'], 
                        attrs['Profit_Margin'], 
                        attrs['Year_Of_Operation'], 
                        attrs['Debt'], 
                        attrs['Company_Valuation'], 
        ]
        knn_data[title] = numeric_values
    return knn_data


def normalize_knn_ready (csv_file, title_col = "Title"):
    lib_file = lib_convert_knn_ready(csv_file, title_col = "Title")
    # Number of numeric positions
    num_pos = len(next(iter(lib_file.values())))
    #Make list for each numeric position
    column = [[] for _ in range(num_pos)]
    for title, values in lib_file.items():
        for i in range (num_pos):
            column[i].append(values[i])
    normalized = []
    for i in range (len(column)):
        minimum = min(column[i])
        maximum = max(column[i])
        norm_col = []
        for j in range (len(column[i])):
            if maximum - minimum == 0:
                norm_val = 0.0
            else:
                norm_val = (column[i][j]-minimum)/(maximum-minimum)
            norm_col.append(round(norm_val, 4))           
        normalized.append(norm_col)
    
    norm_lib_file = {}
    titles = list(lib_file.keys())
    num_feat = len(normalized)
    
    for title in titles:
        norm_lib_file[title] = []
    
    for pos_list, title in enumerate(titles):
        norm_lib_file[title] = [normalized[pos_dic][pos_list] for pos_dic in range (num_feat)]
    
    return norm_lib_file

def unknown_data_normalizer(unknown, csv_file, title_col = "Title"):
    lib_file = lib_convert_knn_ready(csv_file, title_col = "Title")
    num_pos = len(next(iter(lib_file.values())))
    column = [[] for _ in range(num_pos)]
    for title, values in lib_file.items():
        for i in range (num_pos):
            column[i].append(values[i])
    norm_unknown = []
    for i in range (len(column)):
        minimum = min(column[i])
        maximum = max(column[i])
        if maximum - minimum == 0:
            normalized_unknown = 0.0
        else:
            normalized_unknown = (unknown[i]-minimum)/(maximum-minimum)
        norm_unknown.append(round(normalized_unknown, 4))
        
    return norm_unknown

def dif_in_points(pitch1,pitch2):
    diff_sqrd = 0
    for i in range (len(pitch1)):
        diff_sqrd += ((pitch1[i] - pitch2[i]) ** 2)
    diff = diff_sqrd ** 0.5
    return diff

def classify(unknown,dataset_csv, csv_file_labels, k, title_col = "Title"):
    data = normalize_knn_ready(dataset_csv, title_col = "Title")
    unknown_normalized = unknown_data_normalizer(unknown, dataset_csv, title_col = "Title")
    labels_data = lib_convert_knn_ready_labels (csv_file_labels, title_col = "Title")
    distances = []
    titles = list(data.keys())
    for title in titles:
        diff_dis = dif_in_points(data[title], unknown_normalized)
        distances.append([diff_dis, title])
    distances.sort()
    neighbors = distances[0:k]
    sum_shark_deals = 0
    for neighbor in neighbors:
        title = neighbor[1]
        sum_shark_deals += labels_data[title][0]
    avg_shark_deal = round((sum_shark_deals/k),0)
    
    return avg_shark_deal

def accuracy (training_csv, training_labels_csv, validation_csv, validation_labels, k, title_col = "Title"):
    validation_unknown = lib_convert_knn_ready (validation_csv, title_col = "Title")
    validation_unknown_labels = lib_convert_knn_ready_labels (validation_labels, title_col = "Title")
    shark_deals_sum = 0
    validation_sum = 0
    

    for title in validation_unknown:

        validation_sum += 1
        shark_deal_prediction = classify(validation_unknown[title], training_csv, training_labels_csv, k, title_col ="Title" )
        if shark_deal_prediction == validation_unknown_labels[title][0]:
            shark_deals_sum += 1
        else:
            shark_deals_sum += 0
        
            
            
            
    shark_deal_accuracy_avg = shark_deals_sum/validation_sum

    return shark_deal_accuracy_avg


    




#normalized_unknown = unknown_data_normalizer([3000, 100, 2, 3, 0, 7, 1], shark_pitch, title_col = "Title" )


#print (classify(normalized_unknown, shark_pitch, shark_pitch_labels, k = 7, title_col = "Title"))
print(accuracy(shark_pitch,shark_pitch_labels, shark_pitch_val, shark_pitch_val_labels, k = 1, title_col = "Title" ))

    











    



