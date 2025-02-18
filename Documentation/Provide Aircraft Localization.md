# Documentation of Entities and Relationships in Aircraft Localization and Moving-Map System

This document provides a detailed description and interaction overview of various entities and their relationships within an aircraft localization and moving-map system. The primary focus revolves around the handling of aircraft positioning data, its direction, altitude, and the generation and dissemination of a moving map.

## Entities Description

### 1. Aircraft Position
- **Description**: Represents the current geographical location of the aircraft in terms of latitude and longitude.

### 2. Aircraft Direction
- **Description**: Indicates the compass direction in which the aircraft is heading.

### 3. Aircraft Altitude
- **Description**: Represents the height at which the aircraft is flying above sea level, typically measured in feet or meters.

### 4. Moving Map
- **Description**: A dynamic display that updates in real-time to show the aircraft's current position, direction, and altitude on a navigational chart.

### 5. Provide Aircraft Localization
- **Description**: A functional unit responsible for acquiring, processing, and providing the aircraft's current position, direction, and altitude.

### 6. Broadcast Live Moving-Map Channel
- **Description**: This entity takes the aircraft's localization data and generates a live, interactive moving map, which is then broadcasted to relevant recipients.

### 7. Watch Moving Map
- **Description**: Represents the consumers or systems that receive and display the moving map, allowing users to monitor the real-time location and movement of the aircraft.

## Relationships and Data Flows

### Functional Exchanges
1. **Aircraft Position Exchange**
   - **From**: Unknown Source
   - **To**: Unknown Target
   - **Purpose**: Facilitates the transfer of aircraft position data between systems or components.

2. **Aircraft Direction Exchange**
   - **From**: Unknown Source
   - **To**: Unknown Target
   - **Purpose**: Facilitates the transfer of aircraft direction data between systems or components.

3. **Aircraft Altitude Exchange**
   - **From**: Unknown Source
   - **To**: Unknown Target
   - **Purpose**: Facilitates the transfer of aircraft altitude data between systems or components.

4. **Moving Map Exchange**
   - **From**: Unknown Source
   - **To**: Unknown Target
   - **Purpose**: Facilitates the transfer and updating of the moving map data.

### Operational Activities
1. **Outgoing from Provide Aircraft Localization**
   - **Position, Direction, Altitude**
   - **From**: Provide Aircraft Localization
   - **To**: Unknown Target
   - **Purpose**: Outputs the processed localization data (position, direction, altitude) for further use, possibly to the Broadcast Live Moving-Map Channel.

2. **Incoming to Broadcast Live Moving-Map Channel**
   - **Position, Direction, Altitude**
   - **From**: Unknown Source (likely Provide Aircraft Localization)
   - **To**: Broadcast Live Moving-Map Channel
   - **Purpose**: Receives aircraft localization data to generate the live moving map.

3. **Outgoing from Broadcast Live Moving-Map Channel**
   - **Moving Map**
   - **From**: Broadcast Live Moving-Map Channel
   - **To**: Unknown Target (likely Watch Moving Map)
   - **Purpose**: Distributes the generated moving map to consumers or displaying systems.

4. **Incoming to Watch Moving Map**
   - **Moving Map**
   - **From**: Unknown Source (likely Broadcast Live Moving-Map Channel)
   - **To**: Watch Moving Map
   - **Purpose**: Receives and displays the moving map for monitoring purposes.

## Conclusion
This system architecture allows for a robust mechanism where aircraft localization data is continuously processed, transformed into a visual format, and made accessible in real-time to users or systems that require up-to-date navigational information. The relationships defined between entities ensure a smooth flow of data and operational integrity in handling sensitive and critical information about aircraft movements.