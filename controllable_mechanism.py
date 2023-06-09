from block_mechanism import BlockMechanism
from leaf_blocks import CoreBlock

CORE_FORCE = 5000
class ControllableMechansim(BlockMechanism):
    def __init__(self, core_block: CoreBlock, momentum:tuple = (0, 0)):
        super().__init__(core_block, momentum)

    def core_move_up(self, time_between_frame:float) -> None:
        self.add_force((0, -CORE_FORCE), self.get_coor(), time_between_frame)

    def core_move_down(self, time_between_frame:float) -> None:
        self.add_force((0, CORE_FORCE), self.get_coor(), time_between_frame)

    def core_move_left(self, time_between_frame:float) -> None:
        self.add_force((-CORE_FORCE, 0), self.get_coor(), time_between_frame)

    def core_move_right(self, time_between_frame:float) -> None:
        self.add_force((CORE_FORCE, 0), self.get_coor(), time_between_frame)

    def total_hp(self)->float:
        HPs = [bi._hp for bi in self.get_blocks().values()]
        return sum(HPs)

