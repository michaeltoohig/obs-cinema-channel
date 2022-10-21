# TODO

- [x] task to move files from storage to local media directory
- [x] task to remove files from local media directory
- [x] task to update hold media
- [x] check media is available locally before attempting playback
- [ ] fetch a day or more of playlist schedule and run from that
  - [ ] could apscheduler jobs replace asyncio loop?

- [ ] does apscheduler work behind the scenes if started in same script that runs obs?
  - [ ] If yes, remove async file handling for simplicity and won't have to worry about copying files from remote to local blocking an OBS call to the next feature or whatever.

- [x] content_type enum instead of dict
  - [ ] write test

- [ ] confirm too many sessions are not being opened by running playout loop

- [ ] fix bug library copy to local then removes copied files
  - [ ] write test