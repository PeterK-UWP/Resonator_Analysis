"""
This code takes in various data.txt files grabs the respected data, and
plots against the tested variables.

Author - Peter Kveton 2:49 PM 7/2/2025
"""

import matplotlib.pyplot as plt
import numpy as np

def data_read(filename):
    try:
        file = open(filename, 'r')
    except OSError as error:
        print(error)
        return

    content = file.readlines()
    elements = [line.strip() for line in content if line.strip()] # gets rid of spaces between lines
    total_lines = len(elements)
    #print(total_lines)
    #dataf = elements[9:22]#, elements[23:34], elements[36:47], elements[49:60], elements[62:73] # doesnt count last number
    #print(dataf)
    starting_index = 9  # first desired entry
    lines_per_set = 13 # index update number: from simulation lx to ~~~~~
    last_index = starting_index + lines_per_set # 22

    data = []
    while last_index < total_lines:
        data.append(elements[starting_index:last_index])
        # update index
        starting_index = starting_index + lines_per_set
        last_index = last_index + lines_per_set
    else:
        data.append(elements[starting_index:last_index])

    # get rid of '~~~~~' and 'simulation lx'
    for element in data:
        element.pop(0)
        element.pop(-1)
    #print(data)
    return data #total_lines, elements

def categorize(data, filename):
    # get lx data
    file_variable = filename.split('_')[0]
    fixed_values_list = [term[0] for term in data] # grabs fixed values
    #print(file_variable)
    #print(fixed_values_list)

    # get other variables
    data_list = []
    for run in range(len(fixed_values_list)):
        entries = data[run][1:]
        for element in entries:
            variable_value = element.split()
            data_list.append(variable_value)
    #print(data_list)

    # collect variables and test values
    variable_list = []
    variable_values = []
    frequency_values = []
    variables = set()
    for run in data_list:
        key = run[0]
        values = run[1:]
        if key =='fR':
            # collect resultant frequency values
            frequency_values.append(values) # only does the first set
            continue
        if key in variables:
            continue
        variables.add(key)
        variable_values.append(values)
        variable_list.append(key)
    #print(variable_list)
    #print(variable_values)
    #print(frequency_values)

    return file_variable, fixed_values_list, variable_list, variable_values, frequency_values

def pre_plot(fixed_values_list, variable_values, frequency_values):
    # Change Na to np.nan from frequency lists
    new_freq_list = [[np.nan if val == 'Na' else float(val) for val in sublist] for sublist in frequency_values]

    # converts frequency lists into arrays and assigns the array a mask, and collects the masks
    mask_arrays = []
    new_freq_array = []
    for item in new_freq_list:
        array = np.array(item)
        new_freq_array.append(array)
        mask = ~np.isnan(array)
        mask_arrays.append(mask)
    #print(type(new_freq_array[0]))

    # convert variable_values into arrays
    variable_values_array = []
    for item in variable_values:
        array = np.array(item).astype(float)
        variable_values_array.append(array)
    #print(type(variable_values_array[0]))

    # assign mask to variable arrays
    number_of_masks = len(mask_arrays)
    number_of_iterations = len(fixed_values_list)
    step = int(number_of_masks / number_of_iterations)
    sorted_values_array = []
    for index1, array in enumerate(variable_values_array): # 0:wy, 1:w, 2:l_gap, 3:ts, 4:g1
        #print(index1, array)
        masked_values_array = []
        for index2 in range(0, number_of_masks, step):
            masked_index =  index1 + index2
            #print(masked_index)
            #print(array[mask_arrays[masked_index]])
            masked_values_array.append(array[mask_arrays[masked_index]])
        sorted_values_array.append(masked_values_array)
    #print(type(masked_values_array))
    #print(sorted_values_array)

    # assign masks to frequencies and sort similar to masked values array
    masked_frequencies_array_unsorted = []
    for index1, array in enumerate(new_freq_array):  # freq:  0:wy1, 1:w1, 2:l_gap1, 3:ts1, 4:g1_1 5:wy2, ... 24:g1_5
        masked_frequencies_array_unsorted.append(array[mask_arrays[index1]])
   # print(masked_frequencies_array_unsorted)
    sorted_masked_frequencies_array = []
    for index1, array in enumerate(variable_values_array):
        masked_frequencies_array = []
        for index2 in range(0, number_of_masks, step):
            freq_index = index1 + index2
            masked_frequencies_array.append(masked_frequencies_array_unsorted[freq_index])
        sorted_masked_frequencies_array.append(masked_frequencies_array)
    #print(type(masked_frequencies_array_sorted))
    #print(sorted_masked_frequencies_array)

    return sorted_values_array, sorted_masked_frequencies_array

def plot(x_values_array, y_values_array, file_variable, fixed_values_list, variable_list):
    print(fixed_values_list)
    # create legend labels
    legend_labels = []
    for item in fixed_values_list:
        legend_labels.append(f'{file_variable} = {item} \u03bcm')
    #print(legend_labels)

    # create axis labels
    x_labels = []
    for item in variable_list:
        x_labels.append(f'{item} [\u03bcm]')
    y_label = 'fR [THz]'
    #print(x_labels) #, y_label)

    # Setup: 5 subplots in a single figure (3 on top, 2 centered below)
    plt.rcParams['xtick.labelsize'] = 16
    plt.rcParams['ytick.labelsize'] = 16

    fig, axs = plt.subplots(2, 3, figsize=(14, 8))
    axs = axs.flatten()
    fig.suptitle(f'Multivariable Analysis on Resonance by {file_variable}', fontsize=20)
    visual = ['ro-', 'bs-', 'g^-', 'kp-', 'ms-', 'c*-', 'yd-', 'bo-' ]  # Line styles for each curve in a set
    sets = len(x_values_array)
    #print(f"Total sets: {sets}")
    line_handles = []

    for index in range(sets):  # 5 sets
        ax = axs[index]  # 0 to 4 are used for data

        x_group = x_values_array[index]
        y_group = y_values_array[index]
        x_label = x_labels[index]
        y_label_text = y_label

        for i in range(len(fixed_values_list)):  # Each set has n curves
            line, = ax.plot(x_group[i], y_group[i], visual[i], label=legend_labels[i])
            if index == 0:
                line_handles.append(line)  # Only collect handles once

        #ax.set_title(f'Set {index + 1}')
        ax.set_xlabel(x_label, fontsize=16)
        ax.set_ylabel(y_label_text, fontsize=16)

    # Use the 6th subplot for the legend
    legend_ax = axs[5]
    legend_ax.axis('off')  # Hide axis frame and ticks
    legend_ax.legend(handles=line_handles, labels=legend_labels, loc='center', ncol=1, frameon=True, fontsize='large')
    legend_ax.set_title("Legend", fontsize=18)

    plt.tight_layout()
    #plt.show()
    plt.savefig(f'Multivariable Figure {file_variable}')
    return


if __name__ == "__main__":
    files = ['lx_data.txt', 'lgap_data.txt', 'wy_data.txt', 'w_data.txt', 'ts_data.txt', 'g1_data.txt']
    for file in files:
        #categorize(data_read(file), file)
        #pre_plot(categorize(data_read(file), file)[1],
        #         categorize(data_read(file), file)[3],
        #         categorize(data_read(file), file)[4])

        plot(pre_plot(categorize(data_read(file), file)[1],
                      categorize(data_read(file), file)[3],
                      categorize(data_read(file), file)[4])[0],
             pre_plot(categorize(data_read(file), file)[1],
                      categorize(data_read(file), file)[3],
                      categorize(data_read(file), file)[4])[1],
             categorize(data_read(file), file)[0],
             categorize(data_read(file), file)[1],
             categorize(data_read(file), file)[2]
             )
