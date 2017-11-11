function create_schedule(events, number_of_workers)
  events_in_order = order_events(events)
  activities_in_order = order_activities(events_in_order)
  IF activities_in_order is empty THEN
    Error("No activities to schedule")
  ENDIF
  
  calc_early_start_time(events_in_order)
  calc_late_start_time(events_in_order)
  calc_floats(activities_in_order)
  
  critical_path_length = calc_critical_path_length(ordered_activites)
  minimum_workers = calc_minimum_workers(critical_path_length, activities_in_order)
  
  IF number_of_workers > minimum_workers OR number_of_workers = None THEN
    number_of_workers = minimum_workers
  ENDIF
 
END FUNCTION
