import app


# Initialize the multidimensional array of dictionaries
# 0=oflubet 1=sexbet 2=maskülenbet
entries = [
    [{'bet_site': 0, 'betted_by': 'Mert', 'yatirilacak_tutar': 0.0, 'betted_outcome': ''},
     {'bet_site': 1, 'betted_by': 'Mert', 'yatirilacak_tutar': 0.0, 'betted_outcome': ''},
     {'bet_site': 2, 'betted_by': 'Mert', 'yatirilacak_tutar': 0.0, 'betted_outcome': ''}],
    [{'bet_site': 0, 'betted_by': 'Keleş', 'yatirilacak_tutar': 0.0, 'betted_outcome': ''},
     {'bet_site': 1, 'betted_by': 'Keleş', 'yatirilacak_tutar': 0.0, 'betted_outcome': ''},
     {'bet_site': 2, 'betted_by': 'Keleş', 'yatirilacak_tutar': 0.0, 'betted_outcome': ''}],
    [{'bet_site': 0, 'betted_by': 'Semih', 'yatirilacak_tutar': 0.0, 'betted_outcome': ''},
     {'bet_site': 1, 'betted_by': 'Semih', 'yatirilacak_tutar': 0.0, 'betted_outcome': ''},
     {'bet_site': 2, 'betted_by': 'Semih', 'yatirilacak_tutar': 0.0, 'betted_outcome': ''}]
]

def update_entries(preset_num):
    if preset_num == 1:
        entries[0][0]['betted_outcome'] = 1
        entries[0][1]['betted_outcome'] = 0
        entries[0][2]['betted_outcome'] = 2
        entries[1][0]['betted_outcome'] = 2
        entries[1][1]['betted_outcome'] = 1
        entries[1][2]['betted_outcome'] = 0
        entries[2][0]['betted_outcome'] = 0
        entries[2][1]['betted_outcome'] = 2
        entries[2][2]['betted_outcome'] = 1
    elif preset_num == 2:
        entries[0][0]['betted_outcome'] = 2
        entries[0][1]['betted_outcome'] = 0
        entries[0][2]['betted_outcome'] = 1
        entries[1][0]['betted_outcome'] = 1
        entries[1][1]['betted_outcome'] = 2
        entries[1][2]['betted_outcome'] = 0
        entries[2][0]['betted_outcome'] = 0
        entries[2][1]['betted_outcome'] = 1
        entries[2][2]['betted_outcome'] = 2
    elif preset_num == 3:
        entries[0][0]['betted_outcome'] = 0
        entries[0][1]['betted_outcome'] = 1
        entries[0][2]['betted_outcome'] = 2
        entries[1][0]['betted_outcome'] = 1
        entries[1][1]['betted_outcome'] = 2
        entries[1][2]['betted_outcome'] = 0
        entries[2][0]['betted_outcome'] = 2
        entries[2][1]['betted_outcome'] = 0
        entries[2][2]['betted_outcome'] = 1

    for row in range(3):
      for col in range(3):
          if entries[row][col]['bet_site'] == col:
              yatirilacak_tutar = result_table[row][col]
              if entries[row][col]['betted_by'] == 'Mert':
                  entries[row][col]['yatirilacak_tutar'] = yatirilacak_tutar * 4000
              elif entries[row][col]['betted_by'] == 'Keleş':
                  entries[row][col]['yatirilacak_tutar'] = yatirilacak_tutar * 3950
              elif entries[row][col]['betted_by'] == 'Semih':
                entries[row][col]['yatirilacak_tutar'] = yatirilacak_tutar * 3900

# Call this function with the current preset_num



