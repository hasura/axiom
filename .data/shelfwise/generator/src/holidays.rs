use chrono::{Datelike, Duration, NaiveDate, Weekday};
use std::collections::HashMap;

pub fn generate_all_holidays() -> HashMap<String, HashMap<u32, HashMap<String, NaiveDate>>> {
    let mut holidays: HashMap<String, HashMap<u32, HashMap<String, NaiveDate>>> = HashMap::new();
    holidays.insert("us".to_string(), HashMap::new());
    holidays.insert("canada".to_string(), HashMap::new());
    holidays.insert("uk".to_string(), HashMap::new());

    for year in 2010..=2026 {
        // US Holidays
        let mut us_holidays = HashMap::new();
        us_holidays.insert("New Year".to_string(), NaiveDate::from_ymd_opt(year as i32, 1, 1).unwrap());
        us_holidays.insert("MLK Day".to_string(), get_nth_weekday(year, 1, Weekday::Mon, 3));
        us_holidays.insert("Super Bowl Sunday".to_string(), get_first_sunday_february(year));
        us_holidays.insert("Valentine's Day".to_string(), NaiveDate::from_ymd_opt(year as i32, 2, 14).unwrap());
        us_holidays.insert("Presidents Day".to_string(), get_nth_weekday(year, 2, Weekday::Mon, 3));
        us_holidays.insert("Easter".to_string(), calculate_easter(year));
        us_holidays.insert("Memorial Day".to_string(), get_last_monday_may(year));
        us_holidays.insert("Independence Day".to_string(), NaiveDate::from_ymd_opt(year as i32, 7, 4).unwrap());
        us_holidays.insert("Labor Day".to_string(), get_nth_weekday(year, 9, Weekday::Mon, 1));
        us_holidays.insert("Columbus Day".to_string(), get_nth_weekday(year, 10, Weekday::Mon, 2));
        us_holidays.insert("Halloween".to_string(), NaiveDate::from_ymd_opt(year as i32, 10, 31).unwrap());
        us_holidays.insert("Veterans Day".to_string(), NaiveDate::from_ymd_opt(year as i32, 11, 11).unwrap());
        let thanksgiving = get_nth_weekday(year, 11, Weekday::Thu, 4);
        us_holidays.insert("Thanksgiving".to_string(), thanksgiving);
        us_holidays.insert("Black Friday".to_string(), thanksgiving + Duration::days(1));
        us_holidays.insert("Cyber Monday".to_string(), thanksgiving + Duration::days(4));
        us_holidays.insert("Christmas Eve".to_string(), NaiveDate::from_ymd_opt(year as i32, 12, 24).unwrap());
        us_holidays.insert("Christmas".to_string(), NaiveDate::from_ymd_opt(year as i32, 12, 25).unwrap());
        us_holidays.insert("New Years Eve".to_string(), NaiveDate::from_ymd_opt(year as i32, 12, 31).unwrap());
        
        holidays.get_mut("us").unwrap().insert(year as u32, us_holidays);

        // Canada Holidays
        let mut canada_holidays = HashMap::new();
        canada_holidays.insert("New Year".to_string(), NaiveDate::from_ymd_opt(year as i32, 1, 1).unwrap());
        if year >= 2013 {
            canada_holidays.insert("Family Day".to_string(), get_nth_weekday(year, 2, Weekday::Mon, 3));
        }
        let easter = calculate_easter(year);
        canada_holidays.insert("Good Friday".to_string(), easter - Duration::days(2));
        canada_holidays.insert("Easter Monday".to_string(), easter + Duration::days(1));
        canada_holidays.insert("Victoria Day".to_string(), get_monday_before_may_25(year));
        canada_holidays.insert("Canada Day".to_string(), NaiveDate::from_ymd_opt(year as i32, 7, 1).unwrap());
        canada_holidays.insert("Civic Holiday".to_string(), get_nth_weekday(year, 8, Weekday::Mon, 1));
        canada_holidays.insert("Labour Day".to_string(), get_nth_weekday(year, 9, Weekday::Mon, 1));
        canada_holidays.insert("Thanksgiving".to_string(), get_nth_weekday(year, 10, Weekday::Mon, 2));
        canada_holidays.insert("Remembrance Day".to_string(), NaiveDate::from_ymd_opt(year as i32, 11, 11).unwrap());
        canada_holidays.insert("Christmas Eve".to_string(), NaiveDate::from_ymd_opt(year as i32, 12, 24).unwrap());
        canada_holidays.insert("Christmas".to_string(), NaiveDate::from_ymd_opt(year as i32, 12, 25).unwrap());
        canada_holidays.insert("Boxing Day".to_string(), NaiveDate::from_ymd_opt(year as i32, 12, 26).unwrap());
        canada_holidays.insert("New Years Eve".to_string(), NaiveDate::from_ymd_opt(year as i32, 12, 31).unwrap());
        
        holidays.get_mut("canada").unwrap().insert(year as u32, canada_holidays);

        // UK Holidays
        let mut uk_holidays = HashMap::new();
        uk_holidays.insert("New Year".to_string(), NaiveDate::from_ymd_opt(year as i32, 1, 1).unwrap());
        if NaiveDate::from_ymd_opt(year as i32, 1, 1).unwrap().weekday() == Weekday::Sun {
            uk_holidays.insert("New Year Holiday".to_string(), NaiveDate::from_ymd_opt(year as i32, 1, 2).unwrap());
        }
        uk_holidays.insert("Good Friday".to_string(), easter - Duration::days(2));
        uk_holidays.insert("Easter Monday".to_string(), easter + Duration::days(1));
        uk_holidays.insert("Early May Bank Holiday".to_string(), get_nth_weekday(year, 5, Weekday::Mon, 1));
        uk_holidays.insert("Spring Bank Holiday".to_string(), get_last_monday_may(year));
        uk_holidays.insert("Summer Bank Holiday".to_string(), get_last_monday_august(year));
        uk_holidays.insert("Christmas Eve".to_string(), NaiveDate::from_ymd_opt(year as i32, 12, 24).unwrap());
        uk_holidays.insert("Christmas".to_string(), NaiveDate::from_ymd_opt(year as i32, 12, 25).unwrap());
        uk_holidays.insert("Boxing Day".to_string(), NaiveDate::from_ymd_opt(year as i32, 12, 26).unwrap());
        uk_holidays.insert("New Years Eve".to_string(), NaiveDate::from_ymd_opt(year as i32, 12, 31).unwrap());

        // Special UK holidays
        if year == 2011 {
            uk_holidays.insert("Royal Wedding".to_string(), NaiveDate::from_ymd_opt(2011, 4, 29).unwrap());
        }
        if year == 2012 {
            uk_holidays.insert("Diamond Jubilee".to_string(), NaiveDate::from_ymd_opt(2012, 6, 5).unwrap());
        }
        if year == 2022 {
            uk_holidays.insert("Platinum Jubilee".to_string(), NaiveDate::from_ymd_opt(2022, 6, 3).unwrap());
        }
        if year == 2023 {
            uk_holidays.insert("Coronation".to_string(), NaiveDate::from_ymd_opt(2023, 5, 8).unwrap());
        }
        
        holidays.get_mut("uk").unwrap().insert(year as u32, uk_holidays);
    }

    holidays
}

/// Calculate Easter Sunday using the Computus algorithm
pub fn calculate_easter(year: i32) -> NaiveDate {
    let a = year % 19;
    let b = year / 100;
    let c = year % 100;
    let d = b / 4;
    let e = b % 4;
    let f = (b + 8) / 25;
    let g = (b - f + 1) / 3;
    let h = (19 * a + b - d - g + 15) % 30;
    let i = c / 4;
    let k = c % 4;
    let l = (32 + 2 * e + 2 * i - h - k) % 7;
    let m = (a + 11 * h + 22 * l) / 451;
    let month = (h + l - 7 * m + 114) / 31;
    let day = ((h + l - 7 * m + 114) % 31) + 1;
    
    NaiveDate::from_ymd_opt(year as i32, month as u32, day as u32).unwrap()
}

/// Get the nth occurrence of a weekday in a month
pub fn get_nth_weekday(year: i32, month: u32, weekday: Weekday, n: u32) -> NaiveDate {
    let first_day = NaiveDate::from_ymd_opt(year as i32, month, 1).unwrap();
    let first_weekday = first_day.weekday();
    
    let days_until_weekday = ((weekday.num_days_from_monday() as i32 
        - first_weekday.num_days_from_monday() as i32 + 7) % 7) as i64;
    
    let first_occurrence = first_day + Duration::days(days_until_weekday);
    first_occurrence + Duration::weeks((n - 1) as i64)
}

/// Get the last Monday in May
pub fn get_last_monday_may(year: i32) -> NaiveDate {
    let last_day = NaiveDate::from_ymd_opt(year as i32, 5, 31).unwrap();
    let days_back = (last_day.weekday().num_days_from_monday() as i64 + 7) % 7;
    let days_back = if days_back == 0 && last_day.weekday() != Weekday::Mon {
        7
    } else {
        days_back
    };
    last_day - Duration::days(days_back)
}

/// Get the last Monday in August
pub fn get_last_monday_august(year: i32) -> NaiveDate {
    let last_day = NaiveDate::from_ymd_opt(year as i32, 8, 31).unwrap();
    let days_back = (last_day.weekday().num_days_from_monday() as i64 + 7) % 7;
    let days_back = if days_back == 0 && last_day.weekday() != Weekday::Mon {
        7
    } else {
        days_back
    };
    last_day - Duration::days(days_back)
}

/// Get the Monday on or before May 25 (Victoria Day in Canada)
pub fn get_monday_before_may_25(year: i32) -> NaiveDate {
    let may_25 = NaiveDate::from_ymd_opt(year as i32, 5, 25).unwrap();
    let days_back = may_25.weekday().num_days_from_monday() as i64;
    if days_back == 0 {
        may_25
    } else {
        may_25 - Duration::days(days_back)
    }
}

/// Get the first Sunday in February (approximate Super Bowl date)
pub fn get_first_sunday_february(year: i32) -> NaiveDate {
    let first_day = NaiveDate::from_ymd_opt(year as i32, 2, 1).unwrap();
    let days_until_sunday = ((Weekday::Sun.num_days_from_monday() as i32 
        - first_day.weekday().num_days_from_monday() as i32 + 7) % 7) as i64;
    let days_until_sunday = if days_until_sunday == 0 { 7 } else { days_until_sunday };
    first_day + Duration::days(days_until_sunday)
}