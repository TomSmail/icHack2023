# greenship

<img align="right" src='app/web/static/logo.svg' />

Online delivery now dominates shopping habits. Amazon alone carries over 1.6mn packages worldwide per day, which contributes to a phenomenal amount of shipping-induced carbon emissions. In our own city, London, deliveries account for a quarter of all transport-attributable carbon emissions.

Yet, in London alone, over two million commutes take place every day. What if we could harness the regular journeys people make to optimise zero carbon shipping and save the planet?

To achieve this ambition, we present GreenShip, a Progressive Web App to engage everyday commuters in efficient delivery, through monetary incentive. We provide a modular system which can integrate with existing locker infrastructure (e.g. Amazon Lockers) to enable parcel tracking, route planning (using daily travel routes), and courier recompensation. The product is configured to provide accurate estimates of delivery time which can be offered to retailers through an API interface. 

The routing is performed with a proprietary DP algorithm operating on a directed graph, proceeding from the goal location back towards the start locker, calculating the optimal end-time from this node, with the result being cached in a normalised PostgreSQL database.

A challenge faced during the project was in developing a sufficiently efficient yet (close to) optimal algorithm for the task. Several iterations were devised, involving heuristics, pruning and standard algorithms.

As a team we appreciated the opportunity to gain expertise in backend API development, and independently researching and developing the algorithm.

In particular, it was rewarding to be inspired by Cisco’s challenge to develop a solution which we can be proud of, and which we believe can truly make a difference for the planet’s future.

[This project was created for ICHack 2023, Powered by Cisco]

## License

[MIT](https://choosealicense.com/licenses/mit/)