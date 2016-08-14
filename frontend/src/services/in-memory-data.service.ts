export class InMemoryDataService {
    createDb() {
        let stages = [
            {
                id: 1,
                title: 'Your New Feature 1',
                repo: 'stage34',
                branch: 'issue-1-your-new-feature',
                status: 'paused',
                commits: 34,
                created_ts: 1471156891000,
                connect_info: 'fn31dsk.stage34.org'
            }, {
                id: 2,
                title: 'Your New Feature 2',
                repo: 'stage34',
                branch: 'issue-2-your-new-feature',
                status: 'running',
                commits: 4,
                created_ts: 1471156891000,
                connect_info: 'dbh12dj.stage34.org'
            }, {
                id: 3,
                title: 'Your New Feature 3',
                repo: 'stage34',
                branch: 'issue-3-your-new-feature',
                status: 'running',
                commits: 5,
                created_ts: 1471156691000,
                connect_info: 'j12d933.stage34.org'
            }, {
                id: 4,
                title: 'Your New Feature 4',
                repo: 'stage34',
                branch: 'issue-4-your-new-feature',
                status: 'running',
                commits: 4,
                created_ts: 1471156891000,
                connect_info: 'dwnj18f.stage34.org'
            }, {
                id: 5,
                title: 'Your New Feature 5',
                repo: 'stage34',
                branch: 'issue-5-your-new-feature',
                status: 'running',
                commits: 4,
                created_ts: 1471156821000,
                connect_info: 'dn12dn1.stage34.org'
            }, {
                id: 6,
                title: 'Your New Feature 6',
                repo: 'stage34',
                branch: 'issue-6-your-new-feature',
                status: 'running',
                commits: 4,
                created_ts: 1471151891000,
                connect_info: 'njwed19.stage34.org'
            }, {
                id: 7,
                title: 'Your New Feature 7',
                repo: 'stage34',
                branch: 'issue-7-your-new-feature',
                status: 'running',
                commits: 4,
                created_ts: 1471156891000,
                connect_info: 'njw2an1.stage34.org'
            }, {
                id: 8,
                title: 'Your New Feature 8',
                repo: 'stage34',
                branch: 'issue-8-your-new-feature',
                status: 'running',
                commits: 4,
                created_ts: 1471156891000,
                connect_info: 'njw120j.stage34.org'
            }
        ];
    return { stages };
  }
}
