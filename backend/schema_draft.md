| Encja | Pola (Atrybuty) | Relacje / Uwagi |
| :--- | :--- | :--- |
| **Mountain** | `id`, `name`, `elevation_m`, `prominence_m`, `lat`, `lng`, `range_id` | Należy do jednego `Range`. |
| **Range** | `id`, `name` | Pasmo górskie (np. Beskid Śląski). |
| **Badge** | `id`, `name`, `description`, `icon_url` `rules_url` | Korona / odznaka (np. KGP, PTTK). |
| **MountainBadge** | `mountain_id`, `badge_id` | Relacjaiele-do-wielu (góra w wielu koronalach). |
| **Trip** | `id`, `user_id`, `date`, `gpx_path`, `rating_views`, `rating_effort`, `notes` | Główny wpis z wyjazdu. |
| **TripMountain** | `trip_id`, `mountain_id` | Góry zdobyte podczas wycieczki. |
| **Photo** | `id`, `trip_id`, `file_path`, `type` | Typ: `SUMMIT_PROOF` (morda) lub `ROUTE`. |