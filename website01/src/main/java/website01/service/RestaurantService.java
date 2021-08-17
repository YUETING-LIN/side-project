package website01.service;

import website01.Model.RestaurantSearch;

import java.util.List;

public interface RestaurantService {
   public List<RestaurantSearch> commonSearch(RestaurantSearch restaurantSearch);
   //public List<RestaurantSearch> memberSearch(RestaurantSearch restaurantSearch);
}
