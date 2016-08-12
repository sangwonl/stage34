export class InMemoryDataService {
    createDb() {
        let stages = [
            {
                id: 1,
                title: 'My New Feature',
                repo: 'stage34',
                branch: 'issue-3-my-new-feature',
                status: 'paused',
                created_ts: 1451231234
            }, {
                id: 2,
                title: 'Your New Feature',
                repo: 'stage34',
                branch: 'issue-4-your-new-feature',
                status: 'running',
                created_ts: 1451234567
            }
        ];
    return { stages };
  }
}
