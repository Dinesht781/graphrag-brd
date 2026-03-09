## Core Vertices

1. Project (id, name, repo_url, license)
2. Feature (id, title, description)
3. UserStory (id, description, priority, status)
4. Requirement (id, description, acceptace_criteria, type (Functional / Non-functional))
5. Module (id, name, path)
6. Issue (id, title, description, issue_type (Bug, Task, Enhancement, ..)status, created_at)
7. Release (version, release_date)
8. Developer (id, name, role(developer, ))
9. Document (id, name, type (BRD, README, Manual, ...))
10. DocumentChunk (id, text, embedding_vector, page_number)

## Core Relationships

1. Project → HAS_FEATURE → Feature
2. Feature → HAS_STORY → UserStory
3. UserStory → HAS_REQUIREMENT → Requirement
4. Requirement → IMPLEMENTED_BY → Module
5. Module → PART_OF → Project
6. Project → HAS_RELEASE → Release
7. Project → HAS_ISSUE → Issue
8. Issue → ASSIGNED_TO → Developer
9. Issue → AFFECTS → Module
10. Issue → FIXED_IN → Release
11. Document → BELONGS_TO → Project
12. Document → HAS_CHUNK → DocumentChunk

<!-- 
# Future Scope

 ## Core Vertices

1. Project (id, name, description, status, start_date, end_date, business_unit, repo_url, license)
2. Feature (id, title, description)
3. UserStory (id, description, priority, status)
4. Requirement (id, description, acceptace_criteria, type (Functional / Non-functional))
5. Module (id, name, path, tech_stack)
6. Issue (id, title, description, issue_type (Bug, Task, Enhancement, ..), status, severity, created_at, closed_at)
7. Release (version, release_date)
8. Developer (id, name, role(developer, ), team, skills)
9. Document (id, name, type (BRD, README, Manual, ...))
10. DocumentChunk (id, text, embedding_vector, page_number)

## Core Relationships

1. Project → HAS_FEATURE → Feature
2. Feature → HAS_STORY → UserStory
3. UserStory → HAS_REQUIREMENT → Requirement
4. Requirement → IMPLEMENTED_BY → Module
5. Module → PART_OF → Project
6. Project → HAS_RELEASE → Release
7. Project → HAS_ISSUE → Issue
8. Issue → ASSIGNED_TO → Developer
9. Issue → AFFECTS → Module
10. Issue → FIXED_IN → Release
11. Document → BELONGS_TO → Project
12. Document → HAS_CHUNK → DocumentChunk
13. DocumentChunk → MENTIONS → Requirement
14. DocumentChunk → MENTIONS → Feature
15. DocumentChunk → MENTIONS → Module
 -->

<!--
# VERSION 1
 ## Core Vertices

1. Project
2. Feature
3. UserStory
4. Requirement
5. Module
6. Issue
7. Bug
8. Release
9. Developer

## Core Relationships

1. Project → HAS_FEATURE → Feature
2. Feature → HAS_STORY → UserStory
3. UserStory → HAS_REQUIREMENT → Requirement
4. Requirement → IMPLEMENTED_BY → Module
5. Module → PART_OF → Project
6. Project → HAS_RELEASE → Release
7. Project → HAS_ISSUE → Issue
8. Issue → CLASSIFIED_AS → Bug
9. Issue → ASSIGNED_TO → Developer
10. Bug → AFFECTS → Module
11. Bug → FIXED_IN → Release

 -->
