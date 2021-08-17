package website01.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;
import website01.Model.RestaurantSearch;
import website01.mapper.RestaurantMapper;

import java.util.List;


@Service
@Transactional
public class RestaurantServiceImpl implements RestaurantService {
    @Autowired
    private RestaurantMapper restaurantMapper;

    @Override
    @Transactional(propagation = Propagation.SUPPORTS)
    public List<RestaurantSearch> commonSearch(RestaurantSearch restaurantSearch){
        return restaurantMapper.selectRestaurantResult(restaurantSearch);

    }

}
