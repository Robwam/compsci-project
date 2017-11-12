FUNCTION order_events(events_list)
  NEW list ordered
  source_event = FALSE
  
  FOR event in events_list
    IF event has no dependencies THEN
      source_event = TRUE
    ELSE
      Error("List is invalid")
    ENDIF
  ENDFOR
  
  WHILE events_list is not empty
    FOR event in events_list
      IF all event.dependencies in ordered THEN
        add event to ordered
        remove event from events_list
        event_added = TRUE
      ENDIF
    ENDFOR
    IF event_added == FALSE THEN
      Error("List unorderable")
    ENDIF
  ENDWHILE
  
  RETURN ordered
ENDFUNCTION
      
    
  
