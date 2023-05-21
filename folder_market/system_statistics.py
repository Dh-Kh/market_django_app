from .models_for import RatingStorage, Item_info, Salesman_info

def display_statistics(request):
    check_ratings = RatingStorage.objects.filter(unique_user=request.user.username)
    check_for_r = Item_info.objects.filter(salesman = request.user.username)
    check_for_s = Salesman_info.objects.filter(validator_user = request.user.username)
    mapping_list = []
    res_list = []
    for for_r in check_for_r:
        if for_r.salesman == request.user.username:
            for res in check_ratings:
                res_list.extend([
                    res.rating_storage
                ])
                if for_r.salesman != None:
                    mapping_list.extend([for_r.name])
            
    for s_for in check_for_s:
        mapping_list.append(s_for.username)
                
    if sum(res_list) != 0:
        calc_rating = sum(res_list) / len(res_list)
    else:
        calc_rating = 0
    
    for for_s in check_for_s:
        if for_s.validator_user == request.user.username:
            for_s.rating = calc_rating
            for_s.save()
    
    
    mapping_list.append(calc_rating)
    return list(dict.fromkeys(mapping_list))
        